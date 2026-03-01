let wasm,
  WASM_VECTOR_LEN = 0,
  cachedUint8ArrayMemory0 = null;
function getUint8ArrayMemory0() {
  return (
    (null !== cachedUint8ArrayMemory0 &&
      0 !== cachedUint8ArrayMemory0.byteLength) ||
      (cachedUint8ArrayMemory0 = new Uint8Array(wasm.memory.buffer)),
    cachedUint8ArrayMemory0
  );
}
const cachedTextEncoder =
    "undefined" != typeof TextEncoder
      ? new TextEncoder("utf-8")
      : {
          encode: () => {
            throw Error("TextEncoder not available");
          },
        },
  encodeString =
    "function" == typeof cachedTextEncoder.encodeInto
      ? function (e, t) {
          return cachedTextEncoder.encodeInto(e, t);
        }
      : function (e, t) {
          const n = cachedTextEncoder.encode(e);
          return t.set(n), { read: e.length, written: n.length };
        };
function passStringToWasm0(e, t, n) {
  if (void 0 === n) {
    const n = cachedTextEncoder.encode(e),
      r = t(n.length, 1) >>> 0;
    return (
      getUint8ArrayMemory0()
        .subarray(r, r + n.length)
        .set(n),
      (WASM_VECTOR_LEN = n.length),
      r
    );
  }
  let r = e.length,
    o = t(r, 1) >>> 0;
  const i = getUint8ArrayMemory0();
  let a = 0;
  for (; a < r; a++) {
    const t = e.charCodeAt(a);
    if (t > 127) break;
    i[o + a] = t;
  }
  if (a !== r) {
    0 !== a && (e = e.slice(a)), (o = n(o, r, (r = a + 3 * e.length), 1) >>> 0);
    const t = getUint8ArrayMemory0().subarray(o + a, o + r);
    (a += encodeString(e, t).written), (o = n(o, r, a, 1) >>> 0);
  }
  return (WASM_VECTOR_LEN = a), o;
}
const cachedTextDecoder =
  "undefined" != typeof TextDecoder
    ? new TextDecoder("utf-8", { ignoreBOM: !0, fatal: !0 })
    : {
        decode: () => {
          throw Error("TextDecoder not available");
        },
      };
function getStringFromWasm0(e, t) {
  return (
    (e >>>= 0),
    cachedTextDecoder.decode(getUint8ArrayMemory0().subarray(e, e + t))
  );
}
"undefined" != typeof TextDecoder && cachedTextDecoder.decode();
export function wet(e) {
  let t, n;
  try {
    const r = passStringToWasm0(
        e,
        wasm.__wbindgen_malloc,
        wasm.__wbindgen_realloc
      ),
      o = WASM_VECTOR_LEN,
      i = wasm.wet(r, o);
    return (t = i[0]), (n = i[1]), getStringFromWasm0(i[0], i[1]);
  } finally {
    wasm.__wbindgen_free(t, n, 1);
  }
}
export function wdt(e) {
  let t, n;
  try {
    const r = passStringToWasm0(
        e,
        wasm.__wbindgen_malloc,
        wasm.__wbindgen_realloc
      ),
      o = WASM_VECTOR_LEN,
      i = wasm.wdt(r, o);
    return (t = i[0]), (n = i[1]), getStringFromWasm0(i[0], i[1]);
  } finally {
    wasm.__wbindgen_free(t, n, 1);
  }
}
async function __wbg_load(e, t) {
  if ("function" == typeof Response && e instanceof Response) {
    if ("function" == typeof WebAssembly.instantiateStreaming)
      try {
        return await WebAssembly.instantiateStreaming(e, t);
      } catch (t) {
        if ("application/wasm" == e.headers.get("Content-Type")) throw t;
        console.warn(
          "`WebAssembly.instantiateStreaming` failed because your server does not serve Wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n",
          t
        );
      }
    const n = await e.arrayBuffer();
    return await WebAssembly.instantiate(n, t);
  }
  {
    const n = await WebAssembly.instantiate(e, t);
    return n instanceof WebAssembly.Instance ? { instance: n, module: e } : n;
  }
}
function __wbg_get_imports() {
  const e = { wbg: {} };
  return (
    (e.wbg.__wbindgen_init_externref_table = function () {
      const e = wasm.__wbindgen_export_0,
        t = e.grow(4);
      e.set(0, void 0),
        e.set(t + 0, void 0),
        e.set(t + 1, null),
        e.set(t + 2, !0),
        e.set(t + 3, !1);
    }),
    e
  );
}
// eslint-disable-next-line @typescript-eslint/no-empty-function
function __wbg_init_memory(e, t) {}
function __wbg_finalize_init(e, t) {
  return (
    (wasm = e.exports),
    (__wbg_init.__wbindgen_wasm_module = t),
    (cachedUint8ArrayMemory0 = null),
    wasm.__wbindgen_start(),
    wasm
  );
}
function initSync(e) {
  if (void 0 !== wasm) return wasm;
  void 0 !== e &&
    (Object.getPrototypeOf(e) === Object.prototype
      ? ({ module: e } = e)
      : console.warn(
          "using deprecated parameters for `initSync()`; pass a single object instead"
        ));
  const t = __wbg_get_imports();
  __wbg_init_memory(t),
    e instanceof WebAssembly.Module || (e = new WebAssembly.Module(e));
  return __wbg_finalize_init(new WebAssembly.Instance(e, t), e);
}
async function __wbg_init(e) {
  if (void 0 !== wasm) return wasm;
  void 0 !== e &&
    (Object.getPrototypeOf(e) === Object.prototype
      ? ({ module_or_path: e } = e)
      : console.warn(
          "using deprecated parameters for the initialization function; pass a single object instead"
        )),
    void 0 === e && (e = "https://www.yzczb.com/272f6ade9a2ace8d.wasm");
  const t = __wbg_get_imports();
  ("string" == typeof e ||
    ("function" == typeof Request && e instanceof Request) ||
    ("function" == typeof URL && e instanceof URL)) &&
    (e = fetch(e)),
    __wbg_init_memory(t);
  const { instance: n, module: r } = await __wbg_load(await e, t);
  return __wbg_finalize_init(n, r);
}
export { initSync };
export default __wbg_init;
