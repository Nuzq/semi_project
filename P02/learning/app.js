(function () {
  "use strict";

  const root = document.querySelector("[data-p02-root]");
  if (!root) return;

  const documentDialog = document.querySelector("#document-dialog");
  const documentFrame = document.querySelector("#document-frame");
  const documentTitle = document.querySelector("#document-dialog-title");
  const documentClose = document.querySelector("[data-close-document]");
  let lastDocumentTrigger = null;
  let documentCleanupTimer = 0;
  if (documentDialog && documentFrame && documentTitle) {
    root.querySelectorAll("[data-doc-src]").forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        window.clearTimeout(documentCleanupTimer);
        lastDocumentTrigger = trigger;
        documentTitle.textContent = trigger.dataset.docTitle || "文档预览";
        documentFrame.title = documentTitle.textContent;
        documentFrame.src = trigger.dataset.docSrc;
        if (!documentDialog.open) documentDialog.showModal();
        if (documentClose) documentClose.focus();
      });
    });
    if (documentClose) {
      documentClose.addEventListener("click", function () { documentDialog.close(); });
    }
    documentDialog.addEventListener("click", function (event) {
      if (event.target === documentDialog) documentDialog.close();
    });
    documentDialog.addEventListener("close", function () {
      documentCleanupTimer = window.setTimeout(function () {
        if (!documentDialog.open) documentFrame.removeAttribute("src");
      }, 400);
      if (lastDocumentTrigger && document.contains(lastDocumentTrigger)) lastDocumentTrigger.focus();
    });
  }

  const termDefinitions = {
    wdep: {
      symbol: "W_dep",
      english: "Depletion-region width",
      chinese: "耗尽区宽度：PN 结中自由载流子明显减少区域的总宽度。",
      unit: "m",
      role: "外加偏置会改变它；反偏时通常变宽，正偏时通常变窄。"
    },
    epss: {
      symbol: "ε_s",
      english: "Semiconductor permittivity",
      chinese: "半导体介电率：描述材料响应电场的能力。",
      unit: "F/m",
      role: "不是无单位的相对介电常数；通常由 ε_r × ε_0 得到。"
    },
    q: {
      symbol: "q",
      english: "Elementary charge",
      chinese: "元电荷量：基本电荷的正值大小；电子本身的电荷为 −q。",
      unit: "C",
      role: "连接电荷、能量和电压等物理量。"
    },
    na: {
      symbol: "N_A",
      english: "Acceptor concentration",
      chinese: "受主浓度：p 型区域中受主掺杂原子的数密度。",
      unit: "m⁻³（代码统一单位）",
      role: "与 N_D 一起决定 PN 结内建电势和耗尽层分布。"
    },
    nd: {
      symbol: "N_D",
      english: "Donor concentration",
      chinese: "施主浓度：n 型区域中施主掺杂原子的数密度。",
      unit: "m⁻³（代码统一单位）",
      role: "与 N_A 一起决定 PN 结内建电势和耗尽层分布。"
    },
    vbi: {
      symbol: "V_bi",
      english: "Built-in potential",
      chinese: "内建电势：p、n 材料接触并达到热平衡后形成的内部势垒电压。",
      unit: "V",
      role: "耗尽层宽度公式中的结区势垒基线。"
    },
    va: {
      symbol: "V_a",
      english: "Applied junction voltage",
      chinese: "外加结电压：约定 V_a = V_p − V_n，即 p 侧电势减 n 侧电势；正值表示正向偏置。",
      unit: "V（本页面滑块只显示方向和相对强度）",
      role: "正偏时势垒近似为 V_bi−V_a；反偏时 V_a 为负，因而势垒增大。"
    },
    is: {
      symbol: "I_S",
      english: "Reverse saturation current",
      chinese: "反向饱和电流：理想二极管方程中的尺度参数；本页算例将它作为教学假设输入。",
      unit: "A",
      role: "会影响同一正向电流所需的电压；不等同于真实器件中全部反向漏电或击穿电流。"
    },
    ideality: {
      symbol: "n_d",
      english: "Diode ideality factor",
      chinese: "二极管理想因子：调整理想指数关系斜率的无量纲参数。",
      unit: "无量纲",
      role: "理想扩散基线常取 1；不是 MOSFET 的阈值或几何参数。"
    },
    vthermal: {
      symbol: "V_thermal",
      english: "Thermal voltage",
      chinese: "热电压：由热能尺度 k_B·T 除以元电荷 q 得到。",
      unit: "V（常以 mV 表示）",
      role: "随绝对温度 T 成正比；它不是 MOSFET 阈值电压 V_th，也不是外加电源。"
    },
    kb: {
      symbol: "k_B",
      english: "Boltzmann constant",
      chinese: "玻尔兹曼常数：将绝对温度关联到热能尺度的基本物理常数。",
      unit: "J/K",
      role: "与温度 T 相乘得到能量尺度 k_B·T。"
    },
    temperature: {
      symbol: "T",
      english: "Thermodynamic temperature (absolute temperature)",
      chinese: "热力学温度/绝对温度；描述热状态的温度，不能直接使用摄氏度数值。",
      unit: "K（kelvin，开尔文）",
      role: "V_thermal 与 T 成正比；本教学滑块仅展示这一关系。"
    },
    vi: {
      symbol: "V_diode",
      english: "Diode voltage",
      chinese: "二极管端电压：PN 结二极管两端的外加电压。",
      unit: "V",
      role: "代入理想二极管 I–V 方程后，决定指数项的大小。"
    },
    ni: {
      symbol: "n_i",
      english: "Intrinsic carrier concentration",
      chinese: "本征载流子浓度：无掺杂半导体中电子和空穴浓度的基准量。",
      unit: "m⁻³（代码统一单位）",
      role: "它参与内建电势和费米势关系；会随材料和温度变化。"
    },
    epsox: {
      symbol: "ε_ox",
      english: "Oxide permittivity",
      chinese: "氧化物介电率：描述栅氧材料在电场中的极化响应。",
      unit: "F/m",
      role: "与氧化层厚度共同决定单位面积栅氧电容 C_ox。"
    },
    tox: {
      symbol: "t_ox",
      english: "Oxide thickness",
      chinese: "氧化层厚度：栅极与半导体表面之间的绝缘层厚度。",
      unit: "m",
      role: "在 C_ox = ε_ox/t_ox 中，厚度越小，理想单位面积电容越大。"
    },
    phif: {
      symbol: "φ_F",
      english: "Fermi potential",
      chinese: "费米势：这里采用 p 型衬底的正值定义，反映掺杂对能级位置的影响。",
      unit: "V",
      role: "进入阈值电压关系；与温度和衬底掺杂有关。"
    },
    vfb: {
      symbol: "V_FB",
      english: "Flat-Band Voltage",
      chinese: "平带电压：MOS 结构半导体能带近似平直时对应的栅极电压。",
      unit: "V",
      role: "受栅/半导体功函数差及界面电荷等因素影响。"
    },
    idiode: {
      symbol: "I_diode",
      english: "Diode current",
      chinese: "二极管电流：理想 PN 结 I–V 关系计算的端电流。",
      unit: "A",
      role: "是公式输出；并非真实器件测试数据。"
    },
    id: {
      symbol: "I_D",
      english: "Drain current",
      chinese: "漏极电流：MOSFET 漏源沟道中的电流。",
      unit: "A",
      role: "线性区和饱和区公式给出其与端口电压、器件参数的关系。"
    },
    vds: {
      symbol: "V_DS",
      english: "Drain-to-Source Voltage",
      chinese: "漏—源电压：漏极相对源极的电压。",
      unit: "V",
      role: "与过驱动电压 V_OV 比较，判断长沟道模型的工作区。"
    },
    beta: {
      symbol: "β",
      english: "MOSFET transconductance parameter",
      chinese: "MOSFET 跨导参数组合：β = μ_n·C_ox·(W_ch/L_ch)。",
      unit: "A/V²",
      role: "把迁移率、单位面积栅氧电容和沟道几何合并为电流尺度。"
    },
    vov: {
      symbol: "V_OV",
      english: "Overdrive voltage",
      chinese: "过驱动电压：栅—源电压高于阈值电压的部分。",
      unit: "V",
      role: "V_OV = V_GS − V_th；它决定强反型沟道的理想模型边界。"
    },
    vgs: {
      symbol: "V_GS",
      english: "Gate-to-Source Voltage",
      chinese: "栅—源电压：栅极相对源极的电压。",
      unit: "V",
      role: "通过电场控制表面载流子和反型沟道。"
    },
    vth: {
      symbol: "V_th",
      english: "Threshold voltage",
      chinese: "阈值电压：基础 nMOS 模型中形成强反型沟道的近似门槛。",
      unit: "V",
      role: "V_GS 超过它的余量是 V_OV；它不等于热电压。"
    },
    cox: {
      symbol: "C_ox",
      english: "Oxide capacitance per unit area",
      chinese: "单位面积栅氧电容：衡量栅极通过氧化层耦合电荷的能力。",
      unit: "F/m²",
      role: "基础关系 C_ox = ε_ox / t_ox；不能误当作器件总电容。"
    },
    mu: {
      symbol: "μ_n",
      english: "Electron mobility",
      chinese: "电子迁移率：描述电子在电场作用下移动的容易程度。",
      unit: "m²/(V·s)",
      role: "在长沟道模型中与 C_ox、沟道宽长比共同决定电流尺度。"
    },
    geometry: {
      symbol: "W_ch / L_ch",
      english: "Channel width / channel length",
      chinese: "沟道宽度 / 沟道长度：描述沟道几何尺寸的比值。",
      unit: "比值无量纲；W_ch、L_ch 各自用 m",
      role: "在其它参数不变时，宽沟道或短沟道会提高基础模型的电流尺度。"
    }
  };

  const subscriptPattern = /([A-Za-z\u0370-\u03FF]+)_([A-Za-z0-9]+(?:,[0-9]+)?)/g;
  function appendFormattedMathText(target, value) {
    const fragment = document.createDocumentFragment();
    let cursor = 0;
    let match;
    while ((match = subscriptPattern.exec(value)) !== null) {
      fragment.append(document.createTextNode(value.slice(cursor, match.index)));
      const symbol = document.createElement("span");
      symbol.className = "math-symbol";
      symbol.append(document.createTextNode(match[1]));
      const subscript = document.createElement("sub");
      subscript.textContent = match[2];
      symbol.append(subscript);
      fragment.append(symbol);
      cursor = match.index + match[0].length;
    }
    fragment.append(document.createTextNode(value.slice(cursor)));
    target.append(fragment);
    subscriptPattern.lastIndex = 0;
  }

  root.addEventListener("click", function (event) {
    const termButton = event.target.closest("[data-term]");
    if (!termButton || !root.contains(termButton)) return;
    const definition = termDefinitions[termButton.dataset.term];
    if (!definition) return;
    const panel = termButton.closest(".lesson-panel");
    const scopedContainer = termButton.closest("[data-term-scope]");
    const output = scopedContainer
      ? scopedContainer.querySelector("[data-term-output]")
      : panel && panel.querySelector("[data-term-output]");
    if (!output) return;
    const title = document.createElement("strong");
    appendFormattedMathText(title, definition.symbol);
    title.append(document.createTextNode(" — " + definition.english));
    const body = document.createElement("span");
    appendFormattedMathText(body, definition.chinese + " 单位：" + definition.unit + "。用途：" + definition.role);
    output.replaceChildren(title, body);
  });

  const tabs = Array.from(root.querySelectorAll("[data-tab]"));
  function activateTab(tab, moveFocus) {
    tabs.forEach(function (item) {
      const selected = item === tab;
      item.classList.toggle("is-active", selected);
      item.setAttribute("aria-selected", selected ? "true" : "false");
      item.tabIndex = selected ? 0 : -1;
      const panel = root.querySelector("#" + item.dataset.tab);
      if (panel) {
        panel.hidden = !selected;
        panel.classList.toggle("is-active", selected);
      }
    });
    if (moveFocus) tab.focus();
    root.dispatchEvent(new CustomEvent("p02-lesson-change", {
      bubbles: true,
      detail: { panelId: tab.dataset.tab }
    }));
  }
  tabs.forEach(function (tab, index) {
    tab.addEventListener("click", function () { activateTab(tab, false); });
    tab.addEventListener("keydown", function (event) {
      let nextIndex = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") nextIndex = 0;
      else if (event.key === "End") nextIndex = tabs.length - 1;
      else return;
      event.preventDefault();
      activateTab(tabs[nextIndex], true);
    });
  });

  const pnBias = root.querySelector("#pn-bias");
  function updatePN() {
    if (!pnBias) return;
    const bias = Number(pnBias.value);
    const depletion = root.querySelector("#pn-depletion");
    const leftCharge = root.querySelector("#pn-charges-left");
    const rightCharge = root.querySelector("#pn-charges-right");
    const valueLabel = root.querySelector("#pn-bias-value");
    const stateText = root.querySelector("#pn-state-text");
    const stateDot = root.querySelector("#pn-state-dot");
    const width = bias < 0 ? 124 + Math.abs(bias) * 0.79 : Math.max(62, 124 - bias * 0.56);
    if (depletion) {
      depletion.setAttribute("x", String(300 - width / 2));
      depletion.setAttribute("width", String(width));
    }
    if (leftCharge && rightCharge) {
      const leftSigns = Array.from(leftCharge.querySelectorAll("text"));
      const rightSigns = Array.from(rightCharge.querySelectorAll("text"));
      const edgeInset = 6;
      const halfWidth = width / 2;
      const signStep = (halfWidth - edgeInset * 2) / Math.max(1, leftSigns.length - 1);
      leftSigns.forEach(function (sign, index) {
        sign.setAttribute("x", String(300 - halfWidth + edgeInset + index * signStep));
      });
      rightSigns.forEach(function (sign, index) {
        sign.setAttribute("x", String(300 + edgeInset + index * signStep));
      });
    }
    stateDot.classList.remove("is-forward", "is-reverse");
    if (bias < -3) {
      valueLabel.textContent = "反向 " + Math.abs(bias) + "%";
      stateText.textContent = "反向偏置：p 侧接负、n 侧接正；势垒增强，耗尽区在示意图中变宽，尚未考虑击穿。";
      stateDot.classList.add("is-reverse");
    } else if (bias > 3) {
      valueLabel.textContent = "正向 " + bias + "%";
      stateText.textContent = "正向偏置：p 侧接正、n 侧接负；势垒降低、耗尽区变窄，理想二极管电流随正向电压呈指数上升。";
      stateDot.classList.add("is-forward");
    } else {
      valueLabel.textContent = "平衡点";
      stateText.textContent = "热平衡：内建势垒存在，扩散与电场作用平衡，外部净电流为零。";
    }
  }
  if (pnBias) pnBias.addEventListener("input", updatePN);
  updatePN();

  const thermalTemperature = root.querySelector("#thermal-temperature");
  function updateThermalVoltage() {
    if (!thermalTemperature) return;
    const temperature = Number(thermalTemperature.value);
    // Exact SI values for kB and q; these are physical constants, not device-model parameters.
    const boltzmannConstant = 1.380649e-23; // J/K
    const elementaryCharge = 1.602176634e-19; // C
    const thermalVoltageMillivolts = boltzmannConstant * temperature / elementaryCharge * 1e3;
    const temperatureOutput = root.querySelector("#thermal-temp-value");
    const voltageOutput = root.querySelector("#thermal-voltage");
    const meter = root.querySelector(".thermal-meter");
    const fill = root.querySelector("#thermal-fill");
    if (temperatureOutput) temperatureOutput.textContent = temperature.toFixed(0) + " K";
    if (voltageOutput) voltageOutput.textContent = thermalVoltageMillivolts.toFixed(2) + " mV";
    if (meter) {
      meter.setAttribute("aria-valuenow", String(temperature));
      meter.setAttribute("aria-valuetext", temperature.toFixed(0) + " K 时约 " + thermalVoltageMillivolts.toFixed(2) + " mV");
    }
    if (fill) fill.style.width = (temperature / 500 * 100).toFixed(1) + "%";
  }

  const diodeCurrentInput = root.querySelector("#diode-current");
  const diodeSaturationInput = root.querySelector("#diode-saturation-current");
  const diodeIdealityInput = root.querySelector("#diode-ideality");
  function updateDiodeVoltage() {
    const result = root.querySelector("#diode-voltage-result");
    const calculation = root.querySelector("#diode-calculation");
    if (!diodeCurrentInput || !diodeSaturationInput || !diodeIdealityInput || !result || !calculation) return;

    const currentMilliamps = Number(diodeCurrentInput.value);
    const saturationCurrent = Number(diodeSaturationInput.value);
    const ideality = Number(diodeIdealityInput.value);
    const temperature = thermalTemperature ? Number(thermalTemperature.value) : 300;
    if (![currentMilliamps, saturationCurrent, ideality, temperature].every(Number.isFinite) ||
        currentMilliamps < 1e-6 || currentMilliamps > 1000 || saturationCurrent < 1e-30 ||
        saturationCurrent > 1e-3 || ideality < 0.1 || ideality > 3 || temperature < 200 || temperature > 500) {
      result.textContent = "—";
      calculation.textContent = "请把参数调整到输入范围内的正数。";
      return;
    }

    const boltzmannConstant = 1.380649e-23;
    const elementaryCharge = 1.602176634e-19;
    const thermalVoltage = boltzmannConstant * temperature / elementaryCharge;
    const currentAmps = currentMilliamps * 1e-3;
    const currentRatio = currentAmps / saturationCurrent;
    if (!Number.isFinite(currentRatio)) {
      result.textContent = "—";
      calculation.textContent = "当前参数比值超出可计算范围，请调高反向饱和电流或调低正向电流。";
      return;
    }

    const diodeVoltage = ideality * thermalVoltage * Math.log1p(currentRatio);
    result.textContent = diodeVoltage.toFixed(3) + " V";
    calculation.textContent = ideality.toFixed(2) + " × " + (thermalVoltage * 1e3).toFixed(2) +
      " mV × ln(1 + " + currentRatio.toExponential(2) + ") = " + diodeVoltage.toFixed(3) + " V";
  }

  if (thermalTemperature) {
    thermalTemperature.addEventListener("input", function () {
      updateThermalVoltage();
      updateDiodeVoltage();
    });
  }
  [diodeCurrentInput, diodeSaturationInput, diodeIdealityInput].forEach(function (input) {
    if (input) input.addEventListener("input", updateDiodeVoltage);
  });
  updateThermalVoltage();
  updateDiodeVoltage();

  const vovInput = root.querySelector("#mos-vov");
  const vdsInput = root.querySelector("#mos-vds");
  function updateMOS() {
    if (!vovInput || !vdsInput) return;
    const vov = Number(vovInput.value);
    const vds = Number(vdsInput.value);
    const vovOutput = root.querySelector("#mos-vov-value");
    const vdsOutput = root.querySelector("#mos-vds-value");
    const stateText = root.querySelector("#mos-state-text");
    const stateDot = root.querySelector("#mos-state-dot");
    const channel = root.querySelector("#mos-channel");
    const electrons = root.querySelector("#mos-electrons");
    const diagram = root.querySelector(".mos-diagram");
    const curve = root.querySelector("#mos-curve");
    const point = root.querySelector("#mos-curve-point");

    vovOutput.textContent = vov.toFixed(1) + " V（教学刻度）";
    vdsOutput.textContent = vds.toFixed(1) + " V（教学刻度）";
    stateDot.classList.remove("is-forward", "is-reverse");

    let ratio = 0;
    let active = vov > 0;
    if (!active) {
      stateText.textContent = "截止示意：过驱动电压不大于零，强反型沟道未建立；真实器件仍可能有亚阈值电流。";
      channel.setAttribute("points", "184,119 416,119 416,127 184,127");
      channel.setAttribute("opacity", "0.08");
      stateDot.classList.add("is-reverse");
    } else if (vds < vov) {
      ratio = 2 * (vds / vov) - Math.pow(vds / vov, 2);
      stateText.textContent = "线性区：沟道贯通；增加漏—源电压会提高模型电流，器件近似像受栅压控制的电阻。";
      const thickness = Math.min(10, 4 + vov * 2);
      channel.setAttribute("points", "184," + (123 - thickness / 2) + " 416," + (123 - thickness / 2) + " 416," + (123 + thickness / 2) + " 184," + (123 + thickness / 2));
      channel.setAttribute("opacity", "0.92");
    } else {
      ratio = 1;
      stateText.textContent = "饱和区：漏端附近沟道夹断，理想长沟道模型中电流近似饱和；夹断不是击穿。";
      const thickness = Math.min(10, 4 + vov * 2);
      const pinch = Math.max(340, 416 - Math.min(58, 22 + (vds - vov) * 18));
      const half = thickness / 2;
      channel.setAttribute("points", "184," + (123 - half) + " " + pinch + "," + (123 - half) + " 416,123 416,123 " + pinch + "," + (123 + half) + " 184," + (123 + half));
      channel.setAttribute("opacity", "0.92");
      stateDot.classList.add("is-forward");
    }

    if (diagram) diagram.setAttribute("data-active", active && vds > 0 ? "true" : "false");
    if (electrons) electrons.setAttribute("opacity", active && vds > 0 ? "1" : "0");

    let path = "";
    const x0 = 38;
    const x1 = 302;
    const y0 = 118;
    const yTop = 24;
    const maxVds = 2;
    const points = 40;
    for (let i = 0; i <= points; i += 1) {
      const sample = maxVds * i / points;
      let currentRatio = 0;
      if (vov > 0) {
        const x = sample / vov;
        currentRatio = sample <= vov ? Math.max(0, 2 * x - x * x) : 1;
      }
      const xCoord = x0 + (x1 - x0) * sample / maxVds;
      const yCoord = y0 - (y0 - yTop) * currentRatio;
      path += (i === 0 ? "M " : " L ") + xCoord.toFixed(2) + " " + yCoord.toFixed(2);
    }
    curve.setAttribute("d", path);
    const pointX = x0 + (x1 - x0) * vds / maxVds;
    const pointY = y0 - (y0 - yTop) * ratio;
    point.setAttribute("cx", pointX.toFixed(2));
    point.setAttribute("cy", pointY.toFixed(2));
  }
  if (vovInput) vovInput.addEventListener("input", updateMOS);
  if (vdsInput) vdsInput.addEventListener("input", updateMOS);
  updateMOS();

  const unitSpecs = {
    concentration: {
      from: "cm⁻³",
      to: "m⁻³",
      factor: 1e6,
      offset: 0,
      rule: "× 10⁶",
      example: "1e15",
      explanation: "每立方厘米的数量换算为每立方米，数值乘 10⁶。"
    },
    mobility: {
      from: "cm²/(V·s)",
      to: "m²/(V·s)",
      factor: 1e-4,
      offset: 0,
      rule: "× 10⁻⁴",
      example: "1448",
      explanation: "面积单位 cm² 转 m²，换算因子是 10⁻⁴。"
    },
    diffusion: {
      from: "cm²/s",
      to: "m²/s",
      factor: 1e-4,
      offset: 0,
      rule: "× 10⁻⁴",
      example: "10",
      explanation: "扩散系数含长度平方，cm²/s 转为 m²/s 乘 10⁻⁴。"
    },
    length: {
      from: "μm",
      to: "m",
      factor: 1e-6,
      offset: 0,
      rule: "× 10⁻⁶",
      example: "1",
      explanation: "1 μm 等于 10⁻⁶ m。"
    },
    oxide: {
      from: "nm",
      to: "m",
      factor: 1e-9,
      offset: 0,
      rule: "× 10⁻⁹",
      example: "10",
      explanation: "1 nm 等于 10⁻⁹ m。"
    },
    area: {
      from: "cm²",
      to: "m²",
      factor: 1e-4,
      offset: 0,
      rule: "× 10⁻⁴",
      example: "1",
      explanation: "面积换算要把长度换算因子平方：1 cm² = 10⁻⁴ m²。"
    },
    energy: {
      from: "eV",
      to: "J",
      factor: 1.602176634e-19,
      offset: 0,
      rule: "× q ≈ 1.602×10⁻¹⁹",
      example: "1.12",
      explanation: "eV 是能量单位；转换为焦耳时乘元电荷 q。"
    },
    temperature: {
      from: "°C",
      to: "K",
      factor: 1,
      offset: 273.15,
      rule: "+ 273.15",
      example: "25",
      explanation: "摄氏温度转绝对温度：T(K) = T(°C) + 273.15。"
    }
  };
  const unitKind = root.querySelector("#unit-kind");
  const unitInput = root.querySelector("#unit-input");
  function formatNumber(value) {
    if (!Number.isFinite(value)) return "—";
    if (value === 0) return "0";
    const abs = Math.abs(value);
    if (abs >= 1e5 || abs < 1e-3) return value.toExponential(3);
    return Number(value.toPrecision(5)).toLocaleString("en-US");
  }
  function updateUnits(resetExample) {
    if (!unitKind || !unitInput) return;
    const spec = unitSpecs[unitKind.value];
    if (resetExample) unitInput.value = spec.example;
    root.querySelector("#unit-from").textContent = "单位：" + spec.from;
    root.querySelector("#unit-to").textContent = spec.to;
    root.querySelector("#unit-rule").textContent = spec.rule;
    root.querySelector("#unit-explanation").textContent = spec.explanation;
    const inputValue = unitInput.value.trim() === "" ? NaN : Number(unitInput.value);
    const result = inputValue * spec.factor + spec.offset;
    root.querySelector("#unit-result").textContent = formatNumber(result) + " " + spec.to;
  }
  if (unitKind) unitKind.addEventListener("change", function () { updateUnits(true); });
  if (unitInput) unitInput.addEventListener("input", function () { updateUnits(false); });
  updateUnits(false);
}());
