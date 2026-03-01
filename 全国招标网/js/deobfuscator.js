const { parse } = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const generate = require('@babel/generator').default;
const type = require("@babel/types");
const fs = require('fs');

const code = fs.readFileSync('./vaptcha-sdk.1.2.35.669f69e6.js', 'utf-8');
const ast = parse(code);


function calculateExpression(node) {
    // 1. 如果是数字字面量 (如 0x2702)
    if (type.isNumericLiteral(node)) {
        return node.value;
    }

    if (type.isBinaryExpression(node)) {
        const left = calculateExpression(node.left);
        const right = calculateExpression(node.right);

        switch (node.operator) {
            case '+': return left + right;
            case '-': return left - right;
            case '*': return left * right;
            case '/': return left / right;
            case '%': return left % right;
            case '^': return left ^ right;
        }
    }

    // 4. 如果是正负号 (如 -0x3439)
    if (type.isUnaryExpression(node) && node.operator === '-') {
        return -calculateExpression(node.argument);
    }

}

traverse(ast, {
    NumericLiteral(path) {
        if (path.node.extra && path.node.extra.raw.startsWith('0x')) {
            delete path.node.extra;
        }
    },

    StringLiteral(path) {
        // 如果节点有 extra 属性（包含原始的转义格式信息）
        if (path.node.extra) {
            // 直接删除 extra 属性
            // Babel generator 在找不到 extra.raw 时，会根据 node.value 生成普通字符串
            delete path.node.extra;
        }
    },

    BinaryExpression(path) {
        const result = calculateExpression(path.node);

        // 如果计算成功且结果是数字，则替换原表达式
        if (typeof result === 'number' && !isNaN(result)) {
            // console.log(`折叠表达式: ${result}`);
            path.replaceWith(type.numericLiteral(result));
        }
    },
});

const output = generate(ast).code;
fs.writeFileSync('./decode.js', output);
