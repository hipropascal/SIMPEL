class LayerRaster {
    constructor(map, image, palette) {
        this.map = map;
        this.image = image;
        this.onmapdiv = document.createElement('div');
        this.onmapdiv
        this.canvas = document.createElement('canvas');
        this.paletteoption = {
            "gas": {
                "colors": ["#052A2B", "#FBF9D8", "#E68D70", "#9B0080", "#190A54", "#150778"],
                "colorsstop": [0, 0.2, 0.4, 0.6, 0.8, 1]
            },
            "temp": {
                "colors": ["#512728", "#BC2A97", "#44D2D5", "#F6FA3A", "#DD4428", "#5B1C42", "#0a0d70"],
                "colorsstop": [0, 0.2, 0.4, 0.6, 0.8, 0.9, 1]
            },
            "rainbow": {
                "colors": ["#0000D4", "#04d0d3", "#01ba04", "#cece00", "#DD0000", "#4B0086", "#260193"],
                "colorsstop": [0, 0.2, 0.25, 0.35, 0.8, 0.9, 1]
            },
            "rainbow2": {
                "colors": ["#004c99", "#004c99", "#0080fc", "#0080fc", "#66b2fd", "#66b2fd", "#66fdff",
                    "#66fdff", "#00f096", "#00f096", "#00d728", "#00d728", "#9afb31", "#9afb31", "#fefd50", "#fefd50", "#fc974f", "#fc974f",
                    "#ff8015", "#ff8015", "#cc1f03", "#cc1f03", "#991402", "#991402"],
                "colorsstop": [0, 5, 5, 10, 10, 20, 20, 30, 30, 45, 45, 60, 60, 80, 80, 100, 100, 150, 150, 200, 200, 300, 300, 400]
            },
            "cloud": {
                "colors": ["#ff5800", "#ff5800", "#222", "#fff"],
                "colorsstop": [0, 0.35, 0.35, 1]
            }
        };
        this.palette = this.paletteoption[palette];
    }

    // METHOD decode : Decode "in data image" to normal raster
    decode() {
        var canvas = document.createElement('canvas');
        canvas.setAttribute('width', img.width);
        canvas.setAttribute('height', img.height);
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, img.width, img.height);
        var im = ctx.getImageData(0, 0, img.width, img.height);
        var imgData = im.data;
        var imInfo = '';
        for (var x = 0; x < imgData.length; x++) {
            if ((x + 1) % 4 === 0) {
                if (imgData[x] === 0)
                    break;
                continue;
            }
            if (String.fromCharCode(imgData[x]) === 'x')
                break;
            imInfo = imInfo + String.fromCharCode(imgData[x]);
        }
        var infos = imInfo.split("|");
        var datatype = infos[0];
        var top, bottom, left, right;
        if (datatype === "UV") {
            var minU = parseFloat(infos[1]);
            var maxU = parseFloat(infos[2]);
            var minV = parseFloat(infos[3]);
            var maxV = parseFloat(infos[4]);
            top = parseFloat(infos[5]);
            bottom = parseFloat(infos[6]);
            left = parseFloat(infos[7]);
            right = parseFloat(infos[8]);
        } else {
            var min = parseFloat(infos[1]);
            var max = parseFloat(infos[2]);
            top = parseFloat(infos[3]);
            bottom = parseFloat(infos[4]);
            left = parseFloat(infos[5]);
            right = parseFloat(infos[6]);
        }
        // Remove decode
        var canvasInitUV = document.createElement('canvas');
        canvasInitUV.setAttribute('width', img.width);
        canvasInitUV.setAttribute('height', img.height);
        var ctxInitUV = canvasInitUV.getContext("2d");
        ctxInitUV.drawImage(img, 0, 0, img.width, img.height);
        ctxInitUV.clearRect(0, 0, img.width, 5);
        var imgUV = new Image;
        imgUV.src = canvasInitUV.toDataURL();

        var colorBar = getColorBar(color);
        var magArr = [];
        var radArr = [];
        var red, green, blue, alpha, U, V, magVal, magv, radVal;
        if (datatype === "UV") {
            for (x = 3; x < imgData.length; x = x + 4) {
                red = imgData[x - 3];
                green = imgData[x - 2];
                alpha = imgData[x];
                if (alpha === 0) {
                    magArr[((x + 1) / 4) - 1] = -99;
                    radArr[((x + 1) / 4) - 1] = -99;
                } else {
                    U = minU + (red / 255 * (maxU - minU));
                    V = minV + (green / 255 * (maxV - minV));
                    magVal = Math.sqrt(Math.pow(U, 2) + Math.pow(V, 2));
                    radVal = Math.atan2(U, V);
                    magArr[((x + 1) / 4) - 1] = magVal;
                    radArr[((x + 1) / 4) - 1] = radVal;
                    // Image pixel color normalize
                    var magratio = (magVal - minmax[0]) / (minmax[1] - minmax[0]);
                    var colratio = Math.floor(256 * magratio) + 1;
                    if (colratio > 256)
                        colratio = 256;
                    if (colratio < 0)
                        colratio = 0;
                    var magcolpos = colratio * 4;
                    imgData[x - 3] = colorBar[magcolpos];
                    imgData[x - 2] = colorBar[magcolpos + 1];
                    imgData[x - 1] = colorBar[magcolpos + 2];
                }
            }
        } else { // RASTER
            for (x = 0; x < imgData.length; x++) {
                if ((x + 1) % 4 === 0) {
                    red = byteString(imgData[x - 3]);
                    green = byteString(imgData[x - 2]);
                    blue = byteString(imgData[x - 1]);
                    magv = parseInt(red + green + blue, 2);
                    magVal = min + (magv / 16777200 * (max - min));
                    magArr[((x + 1) / 4) - 1] = magVal;
                    // Image pixel color normalize
                    var ratio = (magVal - minmax[0]) / (minmax[1] - minmax[0]);
                    var col = Math.floor(256 * ratio) + 1;
                    if (col > 256)
                        col = 256;
                    if (col < 0)
                        col = 0;
                    var colpos = col * 4;
                    imgData[x - 3] = colorBar[colpos];
                    imgData[x - 2] = colorBar[colpos + 1];
                    imgData[x - 1] = colorBar[colpos + 2];
                }
            }
        }
        $(".legend-value-1").html(minmax[0]);
        $(".legend-value-2").html((minmax[0] + minmax[1]) / 2);
        $(".legend-value-3").html(minmax[1]);
        ctx.putImageData(im, 0, 0);
        ctx.clearRect(0, 0, img.width, 5);
        var strPng = canvas.toDataURL();
        var decodedImage = new Image;
        decodedImage.src = strPng;
        return {
            origin: imgUV,
            decodedImage: decodedImage,
            type: datatype,
            magArray: [],
            radArray: [],
            min: minmax[0],
            max: minmax[1],
            minVal: min,
            maxVal: max,
            minU: minU,
            maxU: maxU,
            minV: minV,
            maxV: maxV,
            width: img.width,
            height: img.height,
            bounding: {
                top: top,
                bottom: bottom,
                left: left,
                right: right
            }
        };
    }

    setRaster() {

    }

    colorbar() {

    }

    startanim() {

    }


}


var moveFps, fps;
var particles = 500;
var partArr = new Array(particles * 3).fill(0);

function decodeImage(img, color, rasgrad) {
}

function getColorBar(color) {
    var pals =
    var xcol = pals[color];
    var cvs = document.createElement("canvas");
    cvs.setAttribute("width", 256);
    cvs.setAttribute("height", 1);
    var ctx = cvs.getContext("2d");
    ctx.lineWidth = 10;
    var grad = ctx.createLinearGradient(0, 0, 256, 1);
    for (var x = 0; x < xcol.colors.length; x++) {
        grad.addColorStop(xcol.colorsstop[x] / xcol.colorsstop[xcol.colors.length - 1], xcol.colors[x]);
    }
    ctx.strokeStyle = grad;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(256, 0);
    ctx.stroke();
    var colorBar = ctx.getImageData(0, 0, cvs.width, cvs.height).data;
    $(".legend-color").attr("src", cvs.toDataURL());
    console.log(cvs.toDataURL());
    return (colorBar);
}


var image, rasterObj;

function loadImage() {
    var area = $('#area').val();
    var instrument = $('#instrument').val();
    var param = $('#param').val();
    var instrument_name = $('#instrument').find(":selected").text();
    var param_name = $('#param').find(":selected").text();
    var hour = $('#hour-grid').val().replace(':', '_');
    var date = $('#date-grid').val();
    var imload = '/api/observasi/grid/get_raster/' + area + '/' + instrument + '/' + param + '/' + date + ' ' + hour + '.png';
    image = new Image;
    image.src = imload;
    image.onload = function () {
        var rasgrad = gradient[instrument_name + '|' + param_name];
        rasterObj = decodeImage(image, "rainbow", rasgrad);
        setTimeout(function () {
            doRaster();
        }, 50);
        setTimeout(function () {
            doAnimate();
        }, 50);
    };
    map.on('moveend move', function (e) {
        try {
            clearTimeout(moveFps)
        } catch (e) {
        }
        doRaster();
    });

}

function doRaster() {
    console.log('doRaster');
    var rasterMap = document.getElementById("map-area");
    var canvas = document.getElementById("cvs-raster");
    var canvasUV = document.getElementById("cvs-data");
    canvas.setAttribute("height", $("#map-area").height());
    canvas.setAttribute("width", $("#map-area").width());
    canvasUV.setAttribute("height", $("#map-area").height());
    canvasUV.setAttribute("width", $("#map-area").width());
    var ctx = canvas.getContext("2d");
    var ctxUV = canvasUV.getContext("2d");
    var xy1 = map.latLngToContainerPoint([rasterObj.bounding.top, rasterObj.bounding.left]);
    var xy2 = map.latLngToContainerPoint([rasterObj.bounding.bottom, rasterObj.bounding.right]);
    var mapx = xy1.x;
    var mapy = xy1.y;
    var scaledwidth = xy2.x - xy1.x;
    var originalwidth = rasterObj.width;
    var xscale = originalwidth / scaledwidth;
    var scaledheight = Math.abs(xy1.y - xy2.y);
    var originalheight = rasterObj.height;
    var yscale = originalheight / scaledheight;
    var xcrop = (function () {
        if (xy1.x > 0) {
            return 0;
        } else {
            return Math.abs(mapx * xscale);
        }
    })();
    var ycrop = (function () {
        if (xy1.y > 0) {
            return 0;
        } else {
            return Math.abs(mapy * yscale);
        }
    })();
    var widthcrop = (function () {
        if (xy2.x < canvas.width) {
            return originalwidth;
        } else {
            return (scaledwidth - (xy2.x - canvas.width)) * xscale;
        }
    })();
    var heightcrop = (function () {
        if (xy2.y < canvas.height) {
            return originalheight;
        } else {
            return (scaledheight - (xy2.y - canvas.height)) * yscale;
        }
    })();
    mapx = (xcrop !== 0) ? 0 : mapx;
    mapy = (ycrop !== 0) ? 0 : mapy;
    scaledwidth = scaledwidth - (scaledwidth - (widthcrop / xscale));
    scaledheight = scaledheight - (scaledheight - (heightcrop / yscale));

    ctx.drawImage(rasterObj.decodedImage, xcrop, ycrop, widthcrop, heightcrop, mapx, mapy, scaledwidth, scaledheight);
    var canvasData = ctx.getImageData(0, 0, $("#map-area").width(), $("#map-area").height());
    var pix = canvasData.data;
    for (var i = 0, n = pix.length; i < n; i += 4) {
        if (pix[i + 3] < 100 && pix[i + 3] !== 0) {
            pix[i + 3] = 0;
        } else if (pix[i + 3] !== 0) {
            pix[i + 3] = 255;
        }
    }
    ctx.putImageData(canvasData, 0, 0);
    if (rasterObj.type === "UV") {
        moveFps = setTimeout(function () {
            ctxUV.drawImage(rasterObj.origin, xcrop, ycrop, widthcrop, heightcrop, mapx, mapy, scaledwidth, scaledheight);
            console.log(canvasUV.toDataURL());
            var canvasDataUV = ctxUV.getImageData(0, 0, $("#map-area").width(), $("#map-area").height());
            var pixUV = canvasDataUV.data;
            for (var i = 0, n = pixUV.length; i < n; i += 4) {
                if (pixUV[i + 3] < 100) {
                    pixUV[i + 3] = 0;
                }
            }
            ctxUV.putImageData(canvasDataUV, 0, 0);
            setupAnimLayer();
        }, 500);
    }
}

function setupAnimLayer() {
    var canvas = document.getElementById("cvs-data");
    var ctx = canvas.getContext("2d");
    partArr.fill(0);
    var width = canvas.width;
    var height = canvas.height;
    var curzoom = ctx.getImageData(0, 0, width, height).data;
    var mag = new Array(height * width);
    var rad = new Array(height * width);
    var r, g, a, u, v;
    for (var x = 3; x < curzoom.length; x = x + 4) {
        r = curzoom[x - 3];
        g = curzoom[x - 2];
        a = curzoom[x];
        if (a === 0) {
            mag[(x + 1) / 4] = -99;
            rad[(x + 1) / 4] = -99;
        } else {
            u = rasterObj.minU + r / 255 * (rasterObj.maxU - rasterObj.minU);
            v = rasterObj.minV + g / 255 * (rasterObj.maxV - rasterObj.minV);
            mag[(x + 1) / 4] = Math.sqrt(Math.pow(u, 2) + Math.pow(v, 2));
            rad[(x + 1) / 4] = Math.atan2(u, v);
        }
    }
    rasterObj.magArray = mag;
    rasterObj.radArray = rad;
}

function doAnimate(rasterObj, type) {
    console.log('llll');
    var rasterMap = document.getElementById("map-animate");
    var canvas = document.getElementById("cvs-animate");
    canvas.setAttribute("height", $("#map-area").height());
    canvas.setAttribute("width", $("#map-area").width());
    var ctx = canvas.getContext("2d");
    ctx.strokeStyle = "rgba(255,255,255,1)";
    ctx.lineWidth = 2;
    startAnimate(ctx, canvas, type);
}

function protate(xaxis, yaxis, rad, xrotate, yrotate) {
    var x = xaxis - xrotate;
    var y = yaxis - yrotate;
    var xnew = (x * Math.cos(rad)) + (-y * Math.sin(rad)) + xrotate;
    var ynew = (x * Math.sin(rad)) + (y * Math.cos(rad)) + yrotate;
    return {'x': xnew, 'y': ynew}
}

function startAnimate(ctx, canvas, type) {
    try {
        clearTimeout(fps);
    } catch (e) {
    }
    ctx.save();
    ctx.globalAlpha = .05;
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.restore();
    if (type === "bulk") {
        ctx.lineWidth = 10;
    } else {
        ctx.lineWidth = 1;
    }
    for (var i = 0; i < partArr.length; i = i + 3) {
        if (partArr[i + 2] === 0) {
            partArr[i] = Math.floor(Math.random() * (canvas.width));
            partArr[i + 1] = Math.floor(Math.random() * (canvas.height));
            partArr[i + 2] = Math.floor(Math.random() * (100)) + 100;
            if (type === "bulk")
                partArr[i + 2] = 10;
        }
        var curx = partArr[i];
        var cury = partArr[i + 1];
        var pos = Math.floor(canvas.width * Math.floor(cury)) + Math.floor(curx);
        var lastrad = rasterObj.radArray[pos];
        if (lastrad === -99) {
            partArr[i + 2] = 0;
            continue;
        }
        var lastmag = rasterObj.magArray[pos];
        var magscale = 0.1 + (((lastmag - rasterObj.min) / (rasterObj.max - rasterObj.min)));
        if (type === "bulk") {
            magscale = 0.6;
        }
        // var newpos = protate(curx, cury - magscale, lastrad, curx, cury);
        var newpos = protate(curx, cury + (magscale), lastrad, curx, cury);
        ctx.beginPath();
        ctx.moveTo(curx, cury);
        ctx.lineTo(newpos.x, newpos.y);
        ctx.stroke();
        partArr[i] = newpos.x;
        partArr[i + 1] = newpos.y;
        partArr[i + 2] = partArr[i + 2] - 1;
    }
    if (type === "bulk") {
        fps = setTimeout(function () {
            startAnimate(ctx, canvas, type)
        }, 100)
    } else {
        fps = setTimeout(function () {
            startAnimate(ctx, canvas, type)
        }, 5)
    }

}


function stopAnimate() {
    try {
        clearTimeout(fps);
        partArr.fill(0);
    } catch (e) {
    }
    var rasterMap = document.getElementById("cvs-raster");
    var canvas = document.getElementById("cvs-animate");
    var ctxRaster = rasterMap.getContext("2d");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, rasterMap.clientWidth, rasterMap.clientHeight);
    ctxRaster.clearRect(0, 0, rasterMap.clientWidth, rasterMap.clientHeight);
    map.off('moveend move');
}