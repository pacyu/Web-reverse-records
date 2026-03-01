const { JSDOM } = require('jsdom');
const { createCanvas, Canvas } = require('canvas');

const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
  url: 'https://www.vaptcha.com/#demo',
  runScripts: 'dangerously',
  resources: 'usable'
});

const window = dom.window;
global.window = window;
global.document = window.document;
global.navigator = window.navigator;
global.HTMLCanvasElement = Canvas;

const originalCreateElement = document.createElement.bind(document);

function getComplexCanvasFingerprint(ha) {
    const text = "BrowserLeaks,com <canvas> 1.0" + ha;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx["fontKerning"] = "auto";
    ctx["textRendering"] = "auto";
    ctx["textBaseline"] = "pot".split("").reverse().join("");
    ctx["font"] = "14px 'Arial'";
    ctx["textBaseline"] = "citebahpla".split("").reverse().join("");
    ctx["fillStyle"] = "#f60";
    ctx["fillRect"](125, 1, 62, 20);
    ctx["fillStyle"] = "#069";
    ctx["fillText"](text, 2, 15);
    ctx["fillStyle"] = "rgba(102, 204, 0, 0.7)";
    ctx["fillText"](text, 4, 17);

    console.log(ctx);

    const baseImage = canvas['toDataURL']();
    // console.log(baseImage);
    const image = baseImage["replace"](",46esab;gnp/egami:atad".split("").reverse().join(""), "");
    const bytes = atob(image);
    const crc32fp = bytes["slice"](-16, -12);
    let hex = "";
    for (var i = 0; i < crc32fp["length"]; i++) {
        var code = crc32fp["charCodeAt"](i);
        if (code <= 15) {
          hex += "0";
        }
        hex += code["toString"](16)["toLocaleUpperCase"]();
    }
    return hex;
}

console.log(getComplexCanvasFingerprint('2d68b'));

