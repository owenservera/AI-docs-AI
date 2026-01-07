const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["_build/assets/_...404_-CpNm3d1s.js","_build/assets/web-Dk3DuTfW.js","_build/assets/index-DdmjgUhI.js","_build/assets/HttpStatusCode-qYNerCsA.js","_build/assets/logo-ornate-dark-DH7mkrML.js","_build/assets/_..-BfykJ4fq.css","_build/assets/index-B_kRTKXu.js","_build/assets/icon-DWVQ4cdX.js","_build/assets/email-signup-A4hchZuo.js","_build/assets/server-runtime-BaX_a5Fe.js","_build/assets/action-Dydp0PIg.js","_build/assets/query-CbweHTSc.js","_build/assets/faq-Bb4qaHlc.js","_build/assets/legal-DxQnkfWA.js","_build/assets/store-CZ2oHrP1.js","_build/assets/components-B35fLny7.js","_build/assets/legal-BBCO41N-.css","_build/assets/index-DaG0qXLN.css","_build/assets/temp-DXbWZczr.js","_build/assets/workspace-CqPIQ496.js","_build/assets/dropdown-BoIBam5W.js","_build/assets/dropdown-BwAG2emZ.css","_build/assets/workspace-DFDShfEg.css","_build/assets/_id_-DwQh5EbL.js","_build/assets/index-DQ3gtYbR.js","_build/assets/index-DE41Lxxl.js","_build/assets/index-CLUNkV97.css","_build/assets/index-DA3EjpND.js","_build/assets/index-C22Rkj2l.css","_build/assets/index-Dw_scY3n.js","_build/assets/index-B9Vj8dF6.css","_build/assets/_id_-BqXGBcoW.js","_build/assets/common-_qm7bcBZ.js","_build/assets/_id_-DeH3o-Rr.css","_build/assets/index-z8VJpvew.js","_build/assets/index-ncO9pm1u.css","_build/assets/index-BlhR8HyJ.js","_build/assets/index-C-xp2F9X.css","_build/assets/index-Ct-wXjZd.js","_build/assets/index-XBzuS4q3.css","_build/assets/index-DdUiFu50.js","_build/assets/index-BLFQAY-N.css","_build/assets/index-e0lzLDfQ.js","_build/assets/index-VHYXvfio.css","_build/assets/index-DUZ2fgAV.js","_build/assets/index--R0W6DcE.css","_build/assets/index-Al8OgaI0.js","_build/assets/index-qIxOCzsr.css","_build/assets/index-CW8vXNxz.js","_build/assets/index-C6fsJlvo.css"])))=>i.map(i=>d[i]);
import { h as hydrate, c as children, a as createMemo, b as createComponent, m as memo, g as getOwner, u as untrack, S as Show, o as on, d as createRoot, e as createSignal, f as onCleanup, s as sharedConfig, i as delegateEvents, l as lazy, j as Suspense, k as getNextElement, t as template, n as insert$1, E as ErrorBoundary$1 } from "./web-Dk3DuTfW.js";
import { L as Link, M as Meta, S as Style, a as MetaProvider, T as Title } from "./index-DdmjgUhI.js";
import { c as createBranches, a as createRouterContext, R as RouterContextObj, s as setInPreloadFn, g as getIntent, b as createRouteContext, d as RouteContextObj, m as mockBase, e as createBeforeLeave, k as keepDepth, f as saveCurrentDepth, n as notifyIfNotBlocked } from "./query-CbweHTSc.js";
import { a as actions } from "./action-Dydp0PIg.js";
import { H as HttpStatusCode } from "./HttpStatusCode-qYNerCsA.js";
function mount(fn, el) {
  return hydrate(fn, el);
}
const createRouterComponent = (router) => (props) => {
  const {
    base
  } = props;
  const routeDefs = children(() => props.children);
  const branches = createMemo(() => createBranches(routeDefs(), props.base || ""));
  let context;
  const routerState = createRouterContext(router, branches, () => context, {
    base,
    singleFlight: props.singleFlight,
    transformUrl: props.transformUrl
  });
  router.create && router.create(routerState);
  return createComponent(RouterContextObj.Provider, {
    value: routerState,
    get children() {
      return createComponent(Root, {
        routerState,
        get root() {
          return props.root;
        },
        get preload() {
          return props.rootPreload || props.rootLoad;
        },
        get children() {
          return [memo(() => (context = getOwner()) && null), createComponent(Routes, {
            routerState,
            get branches() {
              return branches();
            }
          })];
        }
      });
    }
  });
};
function Root(props) {
  const location = props.routerState.location;
  const params = props.routerState.params;
  const data = createMemo(() => props.preload && untrack(() => {
    setInPreloadFn(true);
    props.preload({
      params,
      location,
      intent: getIntent() || "initial"
    });
    setInPreloadFn(false);
  }));
  return createComponent(Show, {
    get when() {
      return props.root;
    },
    keyed: true,
    get fallback() {
      return props.children;
    },
    children: (Root2) => createComponent(Root2, {
      params,
      location,
      get data() {
        return data();
      },
      get children() {
        return props.children;
      }
    })
  });
}
function Routes(props) {
  const disposers = [];
  let root;
  const routeStates = createMemo(on(props.routerState.matches, (nextMatches, prevMatches, prev) => {
    let equal = prevMatches && nextMatches.length === prevMatches.length;
    const next = [];
    for (let i = 0, len = nextMatches.length; i < len; i++) {
      const prevMatch = prevMatches && prevMatches[i];
      const nextMatch = nextMatches[i];
      if (prev && prevMatch && nextMatch.route.key === prevMatch.route.key) {
        next[i] = prev[i];
      } else {
        equal = false;
        if (disposers[i]) {
          disposers[i]();
        }
        createRoot((dispose) => {
          disposers[i] = dispose;
          next[i] = createRouteContext(props.routerState, next[i - 1] || props.routerState.base, createOutlet(() => routeStates()[i + 1]), () => {
            const routeMatches = props.routerState.matches();
            return routeMatches[i] ?? routeMatches[0];
          });
        });
      }
    }
    disposers.splice(nextMatches.length).forEach((dispose) => dispose());
    if (prev && equal) {
      return prev;
    }
    root = next[0];
    return next;
  }));
  return createOutlet(() => routeStates() && root)();
}
const createOutlet = (child) => {
  return () => createComponent(Show, {
    get when() {
      return child();
    },
    keyed: true,
    children: (child2) => createComponent(RouteContextObj.Provider, {
      value: child2,
      get children() {
        return child2.outlet();
      }
    })
  });
};
function intercept([value, setValue], get, set) {
  return [value, set ? (v) => setValue(set(v)) : setValue];
}
function createRouter$1(config) {
  let ignore = false;
  const wrap = (value) => typeof value === "string" ? {
    value
  } : value;
  const signal = intercept(createSignal(wrap(config.get()), {
    equals: (a, b) => a.value === b.value && a.state === b.state
  }), void 0, (next) => {
    !ignore && config.set(next);
    if (sharedConfig.registry && !sharedConfig.done) sharedConfig.done = true;
    return next;
  });
  config.init && onCleanup(config.init((value = config.get()) => {
    ignore = true;
    signal[1](wrap(value));
    ignore = false;
  }));
  return createRouterComponent({
    signal,
    create: config.create,
    utils: config.utils
  });
}
function bindEvent(target, type, handler) {
  target.addEventListener(type, handler);
  return () => target.removeEventListener(type, handler);
}
function scrollToHash(hash, fallbackTop) {
  const el = hash && document.getElementById(hash);
  if (el) {
    el.scrollIntoView();
  } else if (fallbackTop) {
    window.scrollTo(0, 0);
  }
}
function setupNativeEvents(preload2 = true, explicitLinks = false, actionBase = "/_server", transformUrl) {
  return (router) => {
    const basePath = router.base.path();
    const navigateFromRoute = router.navigatorFactory(router.base);
    let preloadTimeout;
    let lastElement;
    function isSvg(el) {
      return el.namespaceURI === "http://www.w3.org/2000/svg";
    }
    function handleAnchor(evt) {
      if (evt.defaultPrevented || evt.button !== 0 || evt.metaKey || evt.altKey || evt.ctrlKey || evt.shiftKey) return;
      const a = evt.composedPath().find((el) => el instanceof Node && el.nodeName.toUpperCase() === "A");
      if (!a || explicitLinks && !a.hasAttribute("link")) return;
      const svg = isSvg(a);
      const href = svg ? a.href.baseVal : a.href;
      const target = svg ? a.target.baseVal : a.target;
      if (target || !href && !a.hasAttribute("state")) return;
      const rel = (a.getAttribute("rel") || "").split(/\s+/);
      if (a.hasAttribute("download") || rel && rel.includes("external")) return;
      const url = svg ? new URL(href, document.baseURI) : new URL(href);
      if (url.origin !== window.location.origin || basePath && url.pathname && !url.pathname.toLowerCase().startsWith(basePath.toLowerCase())) return;
      return [a, url];
    }
    function handleAnchorClick(evt) {
      const res = handleAnchor(evt);
      if (!res) return;
      const [a, url] = res;
      const to = router.parsePath(url.pathname + url.search + url.hash);
      const state = a.getAttribute("state");
      evt.preventDefault();
      navigateFromRoute(to, {
        resolve: false,
        replace: a.hasAttribute("replace"),
        scroll: !a.hasAttribute("noscroll"),
        state: state ? JSON.parse(state) : void 0
      });
    }
    function handleAnchorPreload(evt) {
      const res = handleAnchor(evt);
      if (!res) return;
      const [a, url] = res;
      transformUrl && (url.pathname = transformUrl(url.pathname));
      router.preloadRoute(url, a.getAttribute("preload") !== "false");
    }
    function handleAnchorMove(evt) {
      clearTimeout(preloadTimeout);
      const res = handleAnchor(evt);
      if (!res) return lastElement = null;
      const [a, url] = res;
      if (lastElement === a) return;
      transformUrl && (url.pathname = transformUrl(url.pathname));
      preloadTimeout = setTimeout(() => {
        router.preloadRoute(url, a.getAttribute("preload") !== "false");
        lastElement = a;
      }, 20);
    }
    function handleFormSubmit(evt) {
      if (evt.defaultPrevented) return;
      let actionRef = evt.submitter && evt.submitter.hasAttribute("formaction") ? evt.submitter.getAttribute("formaction") : evt.target.getAttribute("action");
      if (!actionRef) return;
      if (!actionRef.startsWith("https://action/")) {
        const url = new URL(actionRef, mockBase);
        actionRef = router.parsePath(url.pathname + url.search);
        if (!actionRef.startsWith(actionBase)) return;
      }
      if (evt.target.method.toUpperCase() !== "POST") throw new Error("Only POST forms are supported for Actions");
      const handler = actions.get(actionRef);
      if (handler) {
        evt.preventDefault();
        const data = new FormData(evt.target, evt.submitter);
        handler.call({
          r: router,
          f: evt.target
        }, evt.target.enctype === "multipart/form-data" ? data : new URLSearchParams(data));
      }
    }
    delegateEvents(["click", "submit"]);
    document.addEventListener("click", handleAnchorClick);
    if (preload2) {
      document.addEventListener("mousemove", handleAnchorMove, {
        passive: true
      });
      document.addEventListener("focusin", handleAnchorPreload, {
        passive: true
      });
      document.addEventListener("touchstart", handleAnchorPreload, {
        passive: true
      });
    }
    document.addEventListener("submit", handleFormSubmit);
    onCleanup(() => {
      document.removeEventListener("click", handleAnchorClick);
      if (preload2) {
        document.removeEventListener("mousemove", handleAnchorMove);
        document.removeEventListener("focusin", handleAnchorPreload);
        document.removeEventListener("touchstart", handleAnchorPreload);
      }
      document.removeEventListener("submit", handleFormSubmit);
    });
  };
}
function Router(props) {
  const getSource = () => {
    const url = window.location.pathname.replace(/^\/+/, "/") + window.location.search;
    const state = window.history.state && window.history.state._depth && Object.keys(window.history.state).length === 1 ? void 0 : window.history.state;
    return {
      value: url + window.location.hash,
      state
    };
  };
  const beforeLeave = createBeforeLeave();
  return createRouter$1({
    get: getSource,
    set({
      value,
      replace,
      scroll,
      state
    }) {
      if (replace) {
        window.history.replaceState(keepDepth(state), "", value);
      } else {
        window.history.pushState(state, "", value);
      }
      scrollToHash(decodeURIComponent(window.location.hash.slice(1)), scroll);
      saveCurrentDepth();
    },
    init: (notify) => bindEvent(window, "popstate", notifyIfNotBlocked(notify, (delta) => {
      if (delta) {
        return !beforeLeave.confirm(delta);
      } else {
        const s = getSource();
        return !beforeLeave.confirm(s.value, {
          state: s.state
        });
      }
    })),
    create: setupNativeEvents(props.preload, props.explicitLinks, props.actionBase, props.transformUrl),
    utils: {
      go: (delta) => window.history.go(delta),
      beforeLeave
    }
  })(props);
}
const scriptRel = "modulepreload";
const assetsURL = function(dep) {
  return "/" + dep;
};
const seen = {};
const __vitePreload = function preload(baseModule, deps, importerUrl) {
  let promise = Promise.resolve();
  if (deps && deps.length > 0) {
    let allSettled = function(promises$2) {
      return Promise.all(promises$2.map((p) => Promise.resolve(p).then((value$1) => ({
        status: "fulfilled",
        value: value$1
      }), (reason) => ({
        status: "rejected",
        reason
      }))));
    };
    document.getElementsByTagName("link");
    const cspNonceMeta = document.querySelector("meta[property=csp-nonce]");
    const cspNonce = cspNonceMeta?.nonce || cspNonceMeta?.getAttribute("nonce");
    promise = allSettled(deps.map((dep) => {
      dep = assetsURL(dep);
      if (dep in seen) return;
      seen[dep] = true;
      const isCss = dep.endsWith(".css");
      const cssSelector = isCss ? '[rel="stylesheet"]' : "";
      if (document.querySelector(`link[href="${dep}"]${cssSelector}`)) return;
      const link = document.createElement("link");
      link.rel = isCss ? "stylesheet" : scriptRel;
      if (!isCss) link.as = "script";
      link.crossOrigin = "";
      link.href = dep;
      if (cspNonce) link.setAttribute("nonce", cspNonce);
      document.head.appendChild(link);
      if (isCss) return new Promise((res, rej) => {
        link.addEventListener("load", res);
        link.addEventListener("error", () => rej(/* @__PURE__ */ new Error(`Unable to preload CSS for ${dep}`)));
      });
    }));
  }
  function handlePreloadError(err$2) {
    const e$1 = new Event("vite:preloadError", { cancelable: true });
    e$1.payload = err$2;
    window.dispatchEvent(e$1);
    if (!e$1.defaultPrevented) throw err$2;
  }
  return promise.then((res) => {
    for (const item of res || []) {
      if (item.status !== "rejected") continue;
      handlePreloadError(item.reason);
    }
    return baseModule().catch(handlePreloadError);
  });
};
const fileRoutes = [{ "page": true, "$component": { "src": "src/routes/[...404].tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./_...404_-CpNm3d1s.js"
), true ? __vite__mapDeps([0,1,2,3,4,5]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./_...404_-CpNm3d1s.js"
), true ? __vite__mapDeps([0,1,2,3,4,5]) : void 0) }, "path": "/*404" }, { "page": true, "$component": { "src": "src/routes/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-B_kRTKXu.js"
), true ? __vite__mapDeps([6,1,2,7,8,9,10,11,12,13,4,14,15,16,17]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-B_kRTKXu.js"
), true ? __vite__mapDeps([6,1,2,7,8,9,10,11,12,13,4,14,15,16,17]) : void 0) }, "path": "/" }, { "page": true, "$component": { "src": "src/routes/temp.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./temp-DXbWZczr.js"
), true ? __vite__mapDeps([18,1,2,4,7,17]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./temp-DXbWZczr.js"
), true ? __vite__mapDeps([18,1,2,4,7,17]) : void 0) }, "path": "/temp" }, { "page": true, "$component": { "src": "src/routes/workspace.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./workspace-CqPIQ496.js"
), true ? __vite__mapDeps([19,1,9,7,14,20,21,11,10,15,22]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./workspace-CqPIQ496.js"
), true ? __vite__mapDeps([19,1,9,7,14,20,21,11,10,15,22]) : void 0) }, "path": "/workspace" }, { "page": true, "$component": { "src": "src/routes/bench/[id].tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./_id_-DwQh5EbL.js"
), true ? __vite__mapDeps([23,1,9,2,11]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./_id_-DwQh5EbL.js"
), true ? __vite__mapDeps([23,1,9,2,11]) : void 0) }, "path": "/bench/:id" }, { "page": true, "$component": { "src": "src/routes/bench/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DQ3gtYbR.js"
), true ? __vite__mapDeps([24,1,9,2,11,15]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DQ3gtYbR.js"
), true ? __vite__mapDeps([24,1,9,2,11,15]) : void 0) }, "path": "/bench/" }, { "page": true, "$component": { "src": "src/routes/brand/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DE41Lxxl.js"
), true ? __vite__mapDeps([25,1,2,13,4,14,11,9,15,16,26]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DE41Lxxl.js"
), true ? __vite__mapDeps([25,1,2,13,4,14,11,9,15,16,26]) : void 0) }, "path": "/brand/" }, { "page": true, "$component": { "src": "src/routes/download/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DA3EjpND.js"
), true ? __vite__mapDeps([27,1,2,13,4,14,11,9,15,16,7,12,28]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DA3EjpND.js"
), true ? __vite__mapDeps([27,1,2,13,4,14,11,9,15,16,7,12,28]) : void 0) }, "path": "/download/" }, { "page": true, "$component": { "src": "src/routes/enterprise/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-Dw_scY3n.js"
), true ? __vite__mapDeps([29,1,2,13,4,14,11,9,15,16,12,30]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-Dw_scY3n.js"
), true ? __vite__mapDeps([29,1,2,13,4,14,11,9,15,16,12,30]) : void 0) }, "path": "/enterprise/" }, { "page": true, "$component": { "src": "src/routes/workspace/[id].tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./_id_-BqXGBcoW.js"
), true ? __vite__mapDeps([31,1,32,9,11,10,15,33]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./_id_-BqXGBcoW.js"
), true ? __vite__mapDeps([31,1,32,9,11,10,15,33]) : void 0) }, "path": "/workspace/:id" }, { "page": true, "$component": { "src": "src/routes/zen/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-z8VJpvew.js"
), true ? __vite__mapDeps([34,1,9,2,13,4,14,11,15,16,8,10,12,7,35]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-z8VJpvew.js"
), true ? __vite__mapDeps([34,1,9,2,13,4,14,11,15,16,8,10,12,7,35]) : void 0) }, "path": "/zen/" }, { "page": true, "$component": { "src": "src/routes/legal/privacy-policy/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-BlhR8HyJ.js"
), true ? __vite__mapDeps([36,1,2,13,4,14,11,9,15,16,37,26]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-BlhR8HyJ.js"
), true ? __vite__mapDeps([36,1,2,13,4,14,11,9,15,16,37,26]) : void 0) }, "path": "/legal/privacy-policy/" }, { "page": true, "$component": { "src": "src/routes/legal/terms-of-service/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-Ct-wXjZd.js"
), true ? __vite__mapDeps([38,1,2,13,4,14,11,9,15,16,39,26]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-Ct-wXjZd.js"
), true ? __vite__mapDeps([38,1,2,13,4,14,11,9,15,16,39,26]) : void 0) }, "path": "/legal/terms-of-service/" }, { "page": true, "$component": { "src": "src/routes/workspace/[id]/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DdUiFu50.js"
), true ? __vite__mapDeps([40,1,14,9,7,11,32,10,20,21,41]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DdUiFu50.js"
), true ? __vite__mapDeps([40,1,14,9,7,11,32,10,20,21,41]) : void 0) }, "path": "/workspace/:id/" }, { "page": true, "$component": { "src": "src/routes/workspace/[id]/billing/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-e0lzLDfQ.js"
), true ? __vite__mapDeps([42,1,9,14,32,11,10,7,43]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-e0lzLDfQ.js"
), true ? __vite__mapDeps([42,1,9,14,32,11,10,7,43]) : void 0) }, "path": "/workspace/:id/billing/" }, { "page": true, "$component": { "src": "src/routes/workspace/[id]/keys/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DUZ2fgAV.js"
), true ? __vite__mapDeps([44,1,9,7,14,32,11,10,45]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-DUZ2fgAV.js"
), true ? __vite__mapDeps([44,1,9,7,14,32,11,10,45]) : void 0) }, "path": "/workspace/:id/keys/" }, { "page": true, "$component": { "src": "src/routes/workspace/[id]/members/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-Al8OgaI0.js"
), true ? __vite__mapDeps([46,1,9,14,20,7,21,11,10,47]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-Al8OgaI0.js"
), true ? __vite__mapDeps([46,1,9,14,20,7,21,11,10,47]) : void 0) }, "path": "/workspace/:id/members/" }, { "page": true, "$component": { "src": "src/routes/workspace/[id]/settings/index.tsx?pick=default&pick=$css", "build": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-CW8vXNxz.js"
), true ? __vite__mapDeps([48,1,9,14,11,10,49]) : void 0), "import": () => __vitePreload(() => import(
  /* @vite-ignore */
  "./index-CW8vXNxz.js"
), true ? __vite__mapDeps([48,1,9,14,11,10,49]) : void 0) }, "path": "/workspace/:id/settings/" }];
const NODE_TYPES = {
  NORMAL: 0,
  WILDCARD: 1,
  PLACEHOLDER: 2
};
function createRouter(options = {}) {
  const ctx = {
    options,
    rootNode: createRadixNode(),
    staticRoutesMap: {}
  };
  const normalizeTrailingSlash = (p) => options.strictTrailingSlash ? p : p.replace(/\/$/, "") || "/";
  if (options.routes) {
    for (const path in options.routes) {
      insert(ctx, normalizeTrailingSlash(path), options.routes[path]);
    }
  }
  return {
    ctx,
    lookup: (path) => lookup(ctx, normalizeTrailingSlash(path)),
    insert: (path, data) => insert(ctx, normalizeTrailingSlash(path), data),
    remove: (path) => remove(ctx, normalizeTrailingSlash(path))
  };
}
function lookup(ctx, path) {
  const staticPathNode = ctx.staticRoutesMap[path];
  if (staticPathNode) {
    return staticPathNode.data;
  }
  const sections = path.split("/");
  const params = {};
  let paramsFound = false;
  let wildcardNode = null;
  let node = ctx.rootNode;
  let wildCardParam = null;
  for (let i = 0; i < sections.length; i++) {
    const section = sections[i];
    if (node.wildcardChildNode !== null) {
      wildcardNode = node.wildcardChildNode;
      wildCardParam = sections.slice(i).join("/");
    }
    const nextNode = node.children.get(section);
    if (nextNode === void 0) {
      if (node && node.placeholderChildren.length > 1) {
        const remaining = sections.length - i;
        node = node.placeholderChildren.find((c) => c.maxDepth === remaining) || null;
      } else {
        node = node.placeholderChildren[0] || null;
      }
      if (!node) {
        break;
      }
      if (node.paramName) {
        params[node.paramName] = section;
      }
      paramsFound = true;
    } else {
      node = nextNode;
    }
  }
  if ((node === null || node.data === null) && wildcardNode !== null) {
    node = wildcardNode;
    params[node.paramName || "_"] = wildCardParam;
    paramsFound = true;
  }
  if (!node) {
    return null;
  }
  if (paramsFound) {
    return {
      ...node.data,
      params: paramsFound ? params : void 0
    };
  }
  return node.data;
}
function insert(ctx, path, data) {
  let isStaticRoute = true;
  const sections = path.split("/");
  let node = ctx.rootNode;
  let _unnamedPlaceholderCtr = 0;
  const matchedNodes = [node];
  for (const section of sections) {
    let childNode;
    if (childNode = node.children.get(section)) {
      node = childNode;
    } else {
      const type = getNodeType(section);
      childNode = createRadixNode({ type, parent: node });
      node.children.set(section, childNode);
      if (type === NODE_TYPES.PLACEHOLDER) {
        childNode.paramName = section === "*" ? `_${_unnamedPlaceholderCtr++}` : section.slice(1);
        node.placeholderChildren.push(childNode);
        isStaticRoute = false;
      } else if (type === NODE_TYPES.WILDCARD) {
        node.wildcardChildNode = childNode;
        childNode.paramName = section.slice(
          3
          /* "**:" */
        ) || "_";
        isStaticRoute = false;
      }
      matchedNodes.push(childNode);
      node = childNode;
    }
  }
  for (const [depth, node2] of matchedNodes.entries()) {
    node2.maxDepth = Math.max(matchedNodes.length - depth, node2.maxDepth || 0);
  }
  node.data = data;
  if (isStaticRoute === true) {
    ctx.staticRoutesMap[path] = node;
  }
  return node;
}
function remove(ctx, path) {
  let success = false;
  const sections = path.split("/");
  let node = ctx.rootNode;
  for (const section of sections) {
    node = node.children.get(section);
    if (!node) {
      return success;
    }
  }
  if (node.data) {
    const lastSection = sections.at(-1) || "";
    node.data = null;
    if (Object.keys(node.children).length === 0 && node.parent) {
      node.parent.children.delete(lastSection);
      node.parent.wildcardChildNode = null;
      node.parent.placeholderChildren = [];
    }
    success = true;
  }
  return success;
}
function createRadixNode(options = {}) {
  return {
    type: options.type || NODE_TYPES.NORMAL,
    maxDepth: 0,
    parent: options.parent || null,
    children: /* @__PURE__ */ new Map(),
    data: options.data || null,
    paramName: options.paramName || null,
    wildcardChildNode: null,
    placeholderChildren: []
  };
}
function getNodeType(str) {
  if (str.startsWith("**")) {
    return NODE_TYPES.WILDCARD;
  }
  if (str[0] === ":" || str === "*") {
    return NODE_TYPES.PLACEHOLDER;
  }
  return NODE_TYPES.NORMAL;
}
const pageRoutes = defineRoutes(fileRoutes.filter((o) => o.page));
function defineRoutes(fileRoutes2) {
  function processRoute(routes2, route, id, full) {
    const parentRoute = Object.values(routes2).find((o) => {
      return id.startsWith(o.id + "/");
    });
    if (!parentRoute) {
      routes2.push({
        ...route,
        id,
        path: id.replace(/\([^)/]+\)/g, "").replace(/\/+/g, "/")
      });
      return routes2;
    }
    processRoute(parentRoute.children || (parentRoute.children = []), route, id.slice(parentRoute.id.length));
    return routes2;
  }
  return fileRoutes2.sort((a, b) => a.path.length - b.path.length).reduce((prevRoutes, route) => {
    return processRoute(prevRoutes, route, route.path, route.path);
  }, []);
}
createRouter({
  routes: fileRoutes.reduce((memo2, route) => {
    if (!containsHTTP(route)) return memo2;
    const path = route.path.replace(/\([^)/]+\)/g, "").replace(/\/+/g, "/").replace(/\*([^/]*)/g, (_, m) => `**:${m}`).split("/").map((s) => s.startsWith(":") || s.startsWith("*") ? s : encodeURIComponent(s)).join("/");
    if (/:[^/]*\?/g.test(path)) {
      throw new Error(`Optional parameters are not supported in API routes: ${path}`);
    }
    if (memo2[path]) {
      throw new Error(`Duplicate API routes for "${path}" found at "${memo2[path].route.path}" and "${route.path}"`);
    }
    memo2[path] = {
      route
    };
    return memo2;
  }, {})
});
function containsHTTP(route) {
  return route["$HEAD"] || route["$GET"] || route["$POST"] || route["$PUT"] || route["$PATCH"] || route["$DELETE"];
}
const components = {};
function createRoutes() {
  function createRoute(route) {
    const component = route.$component && (components[route.$component.src] ??= lazy(route.$component.import));
    return {
      ...route,
      ...route.$$route ? route.$$route.require().route : void 0,
      info: {
        ...route.$$route ? route.$$route.require().route.info : {},
        filesystem: true
      },
      component,
      children: route.children ? route.children.map(createRoute) : void 0
    };
  }
  const routes2 = pageRoutes.map(createRoute);
  return routes2;
}
let routes;
const FileRoutes = () => routes || (routes = createRoutes());
const Favicon = () => {
  return [createComponent(Link, {
    rel: "icon",
    type: "image/png",
    href: "/favicon-96x96.png",
    sizes: "96x96"
  }), createComponent(Link, {
    rel: "shortcut icon",
    href: "/favicon.ico"
  }), createComponent(Link, {
    rel: "apple-touch-icon",
    sizes: "180x180",
    href: "/apple-touch-icon.png"
  }), createComponent(Link, {
    rel: "manifest",
    href: "/site.webmanifest"
  }), createComponent(Meta, {
    name: "apple-mobile-web-app-title",
    content: "OpenCode"
  })];
};
const inter = "/_build/assets/inter-FIwubZjA.woff2";
const ibmPlexMonoRegular = "/_build/assets/BlexMonoNerdFontMono-Regular-DSJ7IWr2.woff2";
const ibmPlexMonoMedium = "/_build/assets/BlexMonoNerdFontMono-Medium-BvtJB5kd.woff2";
const ibmPlexMonoBold = "/_build/assets/BlexMonoNerdFontMono-Bold-B8jzonSj.woff2";
const cascadiaCode = "/_build/assets/CaskaydiaCoveNerdFontMono-Regular-C_H0OSLN.woff2";
const cascadiaCodeBold = "/_build/assets/CaskaydiaCoveNerdFontMono-Bold-CxABrWmj.woff2";
const firaCode = "/_build/assets/FiraCodeNerdFontMono-Regular-io3c92n9.woff2";
const firaCodeBold = "/_build/assets/FiraCodeNerdFontMono-Bold-BjAeM3gJ.woff2";
const hack = "/_build/assets/HackNerdFontMono-Regular-IcpSchWC.woff2";
const hackBold = "/_build/assets/HackNerdFontMono-Bold-BNG4kp7w.woff2";
const inconsolata = "/_build/assets/InconsolataNerdFontMono-Regular-CRHGEvh2.woff2";
const inconsolataBold = "/_build/assets/InconsolataNerdFontMono-Bold-oTRjQesI.woff2";
const intelOneMono = "/_build/assets/IntoneMonoNerdFontMono-Regular-BwjBdmsJ.woff2";
const intelOneMonoBold = "/_build/assets/IntoneMonoNerdFontMono-Bold-BL6LrHzx.woff2";
const jetbrainsMono = "/_build/assets/JetBrainsMonoNerdFontMono-Regular-QVq88ZfU.woff2";
const jetbrainsMonoBold = "/_build/assets/JetBrainsMonoNerdFontMono-Bold-CU80ifuM.woff2";
const mesloLgs = "/_build/assets/MesloLGSNerdFontMono-Regular-j-nTZDWZ.woff2";
const mesloLgsBold = "/_build/assets/MesloLGSNerdFontMono-Bold-CrpVO3ec.woff2";
const robotoMono = "/_build/assets/RobotoMonoNerdFontMono-Regular-DvxS3QZC.woff2";
const robotoMonoBold = "/_build/assets/RobotoMonoNerdFontMono-Bold-DNxuDepp.woff2";
const sourceCodePro = "/_build/assets/SauceCodeProNerdFontMono-Regular-Ba96Bdne.woff2";
const sourceCodeProBold = "/_build/assets/SauceCodeProNerdFontMono-Bold-DloEeUVQ.woff2";
const ubuntuMono = "/_build/assets/UbuntuMonoNerdFontMono-Regular-tdnXLyap.woff2";
const ubuntuMonoBold = "/_build/assets/UbuntuMonoNerdFontMono-Bold-wLXUURqB.woff2";
const MONO_NERD_FONTS = [{
  family: "JetBrains Mono Nerd Font",
  regular: jetbrainsMono,
  bold: jetbrainsMonoBold
}, {
  family: "Fira Code Nerd Font",
  regular: firaCode,
  bold: firaCodeBold
}, {
  family: "Cascadia Code Nerd Font",
  regular: cascadiaCode,
  bold: cascadiaCodeBold
}, {
  family: "Hack Nerd Font",
  regular: hack,
  bold: hackBold
}, {
  family: "Source Code Pro Nerd Font",
  regular: sourceCodePro,
  bold: sourceCodeProBold
}, {
  family: "Inconsolata Nerd Font",
  regular: inconsolata,
  bold: inconsolataBold
}, {
  family: "Roboto Mono Nerd Font",
  regular: robotoMono,
  bold: robotoMonoBold
}, {
  family: "Ubuntu Mono Nerd Font",
  regular: ubuntuMono,
  bold: ubuntuMonoBold
}, {
  family: "Intel One Mono Nerd Font",
  regular: intelOneMono,
  bold: intelOneMonoBold
}, {
  family: "Meslo LGS Nerd Font",
  regular: mesloLgs,
  bold: mesloLgsBold
}];
const monoNerdCss = MONO_NERD_FONTS.map((font) => `
        @font-face {
          font-family: "${font.family}";
          src: url("${font.regular}") format("woff2");
          font-display: swap;
          font-style: normal;
          font-weight: 400;
        }
        @font-face {
          font-family: "${font.family}";
          src: url("${font.bold}") format("woff2");
          font-display: swap;
          font-style: normal;
          font-weight: 700;
        }`).join("");
const Font = () => {
  return [createComponent(Style, {
    children: `
        @font-face {
          font-family: "Inter";
          src: url("${inter}") format("woff2-variations");
          font-display: swap;
          font-style: normal;
          font-weight: 100 900;
        }
        @font-face {
          font-family: "Inter Fallback";
          src: local("Arial");
          size-adjust: 100%;
          ascent-override: 97%;
          descent-override: 25%;
          line-gap-override: 1%;
        }
        @font-face {
          font-family: "IBM Plex Mono";
          src: url("${ibmPlexMonoRegular}") format("woff2");
          font-display: swap;
          font-style: normal;
          font-weight: 400;
        }
        @font-face {
          font-family: "IBM Plex Mono";
          src: url("${ibmPlexMonoMedium}") format("woff2");
          font-display: swap;
          font-style: normal;
          font-weight: 500;
        }
        @font-face {
          font-family: "IBM Plex Mono";
          src: url("${ibmPlexMonoBold}") format("woff2");
          font-display: swap;
          font-style: normal;
          font-weight: 700;
        }
        @font-face {
          font-family: "IBM Plex Mono Fallback";
          src: local("Courier New");
          size-adjust: 100%;
          ascent-override: 97%;
          descent-override: 25%;
          line-gap-override: 1%;
        }
${monoNerdCss}
      `
  }), createComponent(Link, {
    rel: "preload",
    href: inter,
    as: "font",
    type: "font/woff2",
    crossorigin: "anonymous"
  }), createComponent(Link, {
    rel: "preload",
    href: ibmPlexMonoRegular,
    as: "font",
    type: "font/woff2",
    crossorigin: "anonymous"
  })];
};
function App() {
  return createComponent(Router, {
    explicitLinks: true,
    root: (props) => createComponent(MetaProvider, {
      get children() {
        return [createComponent(Title, {
          children: "opencode"
        }), createComponent(Meta, {
          name: "description",
          content: "OpenCode - The open source coding agent."
        }), createComponent(Favicon, {}), createComponent(Font, {}), createComponent(Suspense, {
          get children() {
            return props.children;
          }
        })];
      }
    }),
    get children() {
      return createComponent(FileRoutes, {});
    }
  });
}
var _tmpl$ = /* @__PURE__ */ template(`<span style=font-size:1.5em;text-align:center;position:fixed;left:0px;bottom:55%;width:100%>`);
const ErrorBoundary = (props) => {
  const message = "Error | Uncaught Client Exception";
  return createComponent(ErrorBoundary$1, {
    fallback: (error) => {
      console.error(error);
      return [(() => {
        var _el$ = getNextElement(_tmpl$);
        insert$1(_el$, message);
        return _el$;
      })(), createComponent(HttpStatusCode, {
        code: 500
      })];
    },
    get children() {
      return props.children;
    }
  });
};
function Dummy(props) {
  return props.children;
}
function StartClient() {
  return createComponent(Dummy, {
    get children() {
      return createComponent(Dummy, {
        get children() {
          return createComponent(ErrorBoundary, {
            get children() {
              return createComponent(App, {});
            }
          });
        }
      });
    }
  });
}
mount(() => createComponent(StartClient, {}), document.getElementById("app"));
