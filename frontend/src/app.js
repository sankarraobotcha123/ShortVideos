function copyText(text) {
  if (!navigator.clipboard) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
    return Promise.resolve();
  }
  return navigator.clipboard.writeText(text);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("pre").forEach((pre) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.textContent = "Copy";
    button.addEventListener("click", async () => {
      await copyText(pre.innerText);
      button.textContent = "Copied";
      setTimeout(() => (button.textContent = "Copy"), 1200);
    });
    pre.insertAdjacentElement("afterend", button);
  });

  document.querySelectorAll("textarea[name='script_text']").forEach((textarea) => {
    const counter = document.createElement("span");
    counter.className = "char-counter";
    const update = () => {
      const words = textarea.value.trim() ? textarea.value.trim().split(/\s+/).length : 0;
      counter.textContent = `${words} words`;
    };
    textarea.insertAdjacentElement("afterend", counter);
    textarea.addEventListener("input", update);
    update();
  });

  document.querySelectorAll("input[type='date'][name='entry_date']").forEach((input) => {
    if (!input.value) {
      input.valueAsDate = new Date();
    }
  });
});
