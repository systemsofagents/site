(() => {
  const form = document.querySelector(".command");
  const screen = document.querySelector("#screen");
  const input = form.querySelector("input");
  const output = document.querySelector("#command-output");
  const hint = form.querySelector("button");
  const fs = JSON.parse(document.querySelector("#virtual-files").textContent);
  const home = "/README.md";
  const track = "/tracks/01/README.md";
  const own = key => Object.prototype.hasOwnProperty.call(fs,key);
  let current = home;
  const forRoute = () => location.hash === "#compaction" ? track :
    (Object.keys(fs).find(key => fs[key].url === location.pathname) || home);
  function open(key, options = {}) {
    if (!own(key)) { output.textContent = "File not found. Type ls to list available files."; return; }
    const entry = fs[key];
    current = key;
    const template = document.createElement("template");
    template.innerHTML = entry.html;
    screen.replaceChildren(template.content);
    const echo = screen.querySelector(".file-command code");
    echo.textContent = "cat " + (options.typed || (key === home ? "README.md" : key));
    document.querySelector(".path").textContent = "~/"+(entry.url === "/" ? "" : entry.url.slice(1,-1));
    document.title = entry.title;
    output.textContent = "";
    if (options.history && location.pathname !== entry.url) history.pushState({}, "", entry.url);
    if (options.pushFocus) screen.querySelector("h1")?.focus({preventScroll:true});
  }
  function resolve(arg) {
    if (!arg || /[\\%?#:\s]/.test(arg)) return "";
    const parts = arg.startsWith("/") ? [] : current.split("/").slice(1,-1);
    for (const piece of arg.split("/")) {
      if (!piece || piece === ".") continue;
      if (piece === "..") { if (!parts.length) return ""; parts.pop(); }
      else if (/^[A-Za-z0-9._-]+$/.test(piece)) parts.push(piece);
      else return "";
    }
    const exact = "/"+parts.join("/");
    return own(exact) ? exact : Object.keys(fs).find(key => key.toLowerCase() === exact.toLowerCase());
  }
  function dispatch(text, action = {}) {
    const value = text.trim();
    if (!value) return;
    const [cmd, ...args] = value.split(/\s+/);
    const arg = args.join(" ");
    switch (cmd.toLowerCase()) {
      case "cat":
        open(resolve(arg), {history:true, typed:arg, pushFocus:action.link}); break;
      case "ls":
        if (current === home) output.textContent = "01  Uncapped session\nREADME.md";
        else output.textContent = Object.keys(fs).filter(k=>k.startsWith("/tracks/01/")).map(k=>k.split("/").at(-1)).join("\n");
        break;
      case "open":
        if (["01","001","uncapped session"].includes(arg.toLowerCase())) dispatch("cat "+track,action);
        else output.textContent = "Unknown track. Type ls to see tracks.";
        break;
      case "back":
        if (current === home) output.textContent = "Already at ~/.";
        else dispatch("cat "+(current === track ? home : track),action);
        break;
      case "help":
        output.textContent = "cat README.md  read the current folder’s intro\nls             list tracks or files\nopen 01        open Uncapped session\nback           return up a level\nhelp           show commands";
        break;
      default: output.textContent = "Unknown command. Type help for available commands.";
    }
  }
  screen.addEventListener("click", event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
    const link = event.target.closest("a[data-file]");
    if (!link) return;
    event.preventDefault();
    dispatch("cat "+link.dataset.file,{link:true});
  });
  form.hidden = false;
  form.addEventListener("submit", event => { event.preventDefault(); dispatch(input.value); input.value = ""; });
  hint.addEventListener("click", ()=>dispatch("help"));
  const follow = () => {
    const key = forRoute(); open(key);
    if (location.hash === "#compaction") history.replaceState({}, "", fs[key].url);
  };
  window.addEventListener("popstate", follow);
  window.addEventListener("hashchange", () => { if (location.hash === "#compaction") follow(); });
  follow();
})();
