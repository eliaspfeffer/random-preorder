# Front-view hardware illustration

The image is a layout concept, not a schematic, validated BOM, or proof of entropy quality.

Requested arrangement: one visible PCB; sparse electronics and rechargeable AAA cell on the left, 24-word display on the right. No decorative electronics around the display.

Functional groups that an implementation must resolve:
- Noise source and bias: resistor thermal noise or semiconductor noise. The choice determines bias, gain and bandwidth. A transistor avalanche source may need a separate higher-voltage supply; it cannot simply be assumed to work from a 1.2 V cell.
- Analog amplification/filtering and isolated/buffered oscilloscope test point, so probing does not change the sampled source.
- MCU with ADC, entropy-source health tests and conditioning, and BIP39 encoding with checksum. A word display does not establish sufficient entropy.
- AAA NiMH cell, power switch, boost converter, inductor and local decoupling capacitors; external cell charging is assumed, not an invented onboard charging circuit.
- Display and a separately specified source-code readout interface. A connector alone does not implement read-only behavior.

The generated arrangement uses resistor/capacitor/transistor/chip package shapes to illustrate these groups. Counts, pin routing, exact part numbers and electrical values are deliberately NOT a procurement list. A real minimal BOM requires choosing the entropy architecture, designing the circuit and measuring it. No hardware security or single-cell runtime validation has been performed.

Primary references checked 16 Nov 2026:
- Analog Devices, sources of semiconductor white noise: https://www.analog.com/en/resources/technical-articles/managing-noise-in-the-signal-chain-part-1-annoying-semiconductor-noise-preventable-or-inescapable.html
- TI TPS61099, low-voltage boost converter family (candidate power building block, not a final selection): https://www.ti.com/product/TPS61099
