const { JSDOM } = require('jsdom');
const fs = require('fs');
const vm = require('vm');
const canvas = require('canvas');

function watch(obj, objName) {
    return new Proxy(obj, {
        get(target, prop, receiver) {
            const value = Reflect.get(target, prop, receiver);
            const propName = prop.toString();

            // 过滤掉一些频繁且无关紧要的 Symbol 访问
            if (typeof prop !== 'symbol') {
                console.log(`[GET] ${objName}.${propName} ->`, value === undefined ? 'undefined (缺失!)' : typeof value);
            }

            // 关键：处理方法调用时的 this 指向问题 (修复之前的 ERR_INVALID_THIS)
            if (typeof value === 'function') {
                return value.bind(target);
            }
            return value;
        },
        set(target, prop, value, receiver) {
            console.log(`[SET] ${objName}.${prop.toString()} =`, value);
            return Reflect.set(target, prop, value, receiver);
        }
    });
}

// 注意：启用 runScripts: "dangerously" 是为了允许执行文件中的立即执行函数表达式 (IIFE)
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
    runScripts: "dangerously",
    url: "https://ctbpsp.com/",
    // 确保模拟了必要的 referrer 属性
    referrer: "https://ctbpsp.com/",
    pretendToBeVisual: true, // 这会让 jsdom 模拟更接近浏览器的环境
    // virtualConsole: new dom.window.console.constructor(), // 抑制一些 jsdom 警告
    canvas: "sendback" // 使用 sendback 模式确保 canvas API可用
});

window = dom.window;
document = dom.window.document;
navigator = dom.window.navigator;

screen = {
    // 注入常见的屏幕属性，值可以根据需要模拟一个标准桌面环境
    availHeight: 1040,
    availLeft: 0,
    availTop: 0,
    availWidth: 1920,
    height: 1080,
    width: 1920,
    colorDepth: 24,
    pixelDepth: 24
};

// 3. 读取并执行文件内容
const algorithmCode = fs.readFileSync('./decode.js', 'utf8');


const context = {
    window: window,
    document: document,
    screen: screen,
    setTimeout: setTimeout.bind(globalThis),
    EventTarget: window.EventTarget,
    Request: Request,
    fetch: fetch.bind(globalThis),
    // ... 传入所有需要的全局变量
};

vm.createContext(context);

vm.runInContext(algorithmCode, context, {
    timeout: 5000,
    displayErrors: true
});

console.log(document.cookie)
