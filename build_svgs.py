from pathlib import Path

def build_svg(is_dark=True):
    tspans = Path("portrait_tspan.txt").read_text(encoding="utf-8")
    
    if is_dark:
        # Dark cyberpunk theme
        ascii_grad_stops = """
    <stop offset="0%" stop-color="#22D3EE">
      <animate attributeName="stop-color" values="#22D3EE;#7C3AED;#38BDF8;#22D3EE" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#7C3AED">
      <animate attributeName="stop-color" values="#7C3AED;#38BDF8;#22D3EE;#7C3AED" dur="9s" repeatCount="indefinite"/>
    </stop>"""
        border_grad_stops = """
    <stop offset="0%" stop-color="#7C3AED"/>
    <stop offset="50%" stop-color="#22D3EE"/>
    <stop offset="100%" stop-color="#10B981"/>"""
        bg_glow_stops = """
    <stop offset="0%" stop-color="#0B1120"/>
    <stop offset="100%" stop-color="#050816"/>"""
        scan_grad_stops = """
  <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
  <stop offset="45%" stop-color="#22D3EE" stop-opacity="0.05"/>
  <stop offset="50%" stop-color="#A5F3FC" stop-opacity="0.65"/>
  <stop offset="55%" stop-color="#22D3EE" stop-opacity="0.05"/>
  <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>"""
        scanlines_fill = '#7DD3FC" opacity="0.05'
        titlebar_bg = '#0B1120" fill-opacity="0.85'
        panel_bg = '#0B1120" fill-opacity="0.35'
        text_fill = "#dbeafe"
        
        css_rules = """
    .ascii  { font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }
    .key    { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #22D3EE; font-weight: bold; }
    .value  { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #E5E7EB; }
    .cc     { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #475569; }
    .head   { font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: #7C3AED; font-weight: bold; }
    .accent { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #10B981; font-weight: bold; }
    text, tspan { white-space: pre; }
    
    .term-label { font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #64748B; letter-spacing: 0.5px; }
    .scan-label { font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #F87171; letter-spacing: 1px; }
    .panel-title { font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: #38BDF8; letter-spacing: 2px; opacity: 0.7; }
    .cursor-blink { fill: #22D3EE; }
"""
        scan_overlay = """<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="0.7" style="mix-blend-mode:screen">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>"""
        border_box = """<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.8">
  <animate attributeName="opacity" values="0.5;0.95;0.5" dur="3.2s" repeatCount="indefinite"/>
</rect>"""
    else:
        # Light theme
        ascii_grad_stops = """
    <stop offset="0%" stop-color="#4F46E5">
      <animate attributeName="stop-color" values="#4F46E5;#7C3AED;#0EA5E9;#4F46E5" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#7C3AED">
      <animate attributeName="stop-color" values="#7C3AED;#0EA5E9;#4F46E5;#7C3AED" dur="9s" repeatCount="indefinite"/>
    </stop>"""
        border_grad_stops = """
    <stop offset="0%" stop-color="#7C3AED"/>
    <stop offset="50%" stop-color="#0EA5E9"/>
    <stop offset="100%" stop-color="#059669"/>"""
        bg_glow_stops = """
    <stop offset="0%" stop-color="#F8FAFC"/>
    <stop offset="100%" stop-color="#E2E8F0"/>"""
        scan_grad_stops = """
  <stop offset="0%" stop-color="#0EA5E9" stop-opacity="0"/>
  <stop offset="45%" stop-color="#0EA5E9" stop-opacity="0.06"/>
  <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.55"/>
  <stop offset="55%" stop-color="#0EA5E9" stop-opacity="0.06"/>
  <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>"""
        scanlines_fill = '#334155" opacity="0.035'
        titlebar_bg = '#FFFFFF" fill-opacity="0.9'
        panel_bg = '#FFFFFF" fill-opacity="0.6'
        text_fill = "#1E293B"
        
        css_rules = """
    .ascii  { font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }
    .key    { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #0284C7; font-weight: bold; }
    .value  { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #1E293B; }
    .cc     { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #94A3B8; }
    .head   { font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: #7C3AED; font-weight: bold; }
    .accent { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #059669; font-weight: bold; }
    text, tspan { white-space: pre; }
    
    .term-label { font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #64748B; letter-spacing: 0.5px; }
    .scan-label { font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #DC2626; letter-spacing: 1px; }
    .panel-title { font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: #0284C7; letter-spacing: 2px; opacity: 0.75; }
    .cursor-blink { fill: #0EA5E9; }
"""
        scan_overlay = """<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="0.4" style="mix-blend-mode:multiply">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>"""
        border_box = """<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.6">
  <animate attributeName="opacity" values="0.4;0.8;0.4" dur="3.2s" repeatCount="indefinite"/>
</rect>"""

    # Staggered clip-paths for right panel typing animation
    clip_paths = []
    y_starts = [
        26.00, 50.00, 72.00, 94.00, 116.00, 138.00, 160.00, 182.00,
        204.00, 226.00, 248.00, 270.00, 292.00, 314.00, 336.00, 358.00,
        380.00, 402.00, 424.00, 446.00, 468.00, 490.00
    ]
    begin_t = 0.75
    for i, py in enumerate(y_starts):
        dur = 0.38
        b = round(begin_t + i * 0.115, 2)
        clip_paths.append(f'<clipPath id="lc{i}"><rect x="500" y="{py:.2f}" width="0" height="24"><animate attributeName="width" from="0" to="690" dur="{dur}s" begin="{b}s" fill="freeze"/></rect></clipPath>')
    clip_paths_str = "".join(clip_paths)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">{ascii_grad_stops}
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">{border_grad_stops}
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">{bg_glow_stops}
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">{scan_grad_stops}
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{scanlines_fill}"/>
  </pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="620">
    <rect x="0" y="0" width="1180" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="560" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
    </rect>
  </mask>
  {clip_paths_str}
  <style>{css_rules}  </style>
</defs>

<rect width="1180" height="610" rx="18" fill="url(#bgGlow)"/>
<rect width="1180" height="610" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="{titlebar_bg}"/>
  <circle cx="24" cy="20" r="5" fill="#EF4444"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="#F59E0B"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="#10B981"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">khushboo@devos ~ % ./profile.sh --live</text>
  <circle cx="1122" cy="20" r="4" fill="#F87171">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.1s" repeatCount="indefinite"/>
  </circle>
  <text x="1132" y="24" class="scan-label">SCANNING</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="468" rx="14" fill="{panel_bg}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <rect x="508" y="10" width="655" height="500" rx="14" fill="{panel_bg}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
    <text x="30" y="0" class="ascii">
{tspans}
    </text>
  </g>

  <g clip-path="url(#lc0)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="42" class="head">khushboo@devos</tspan><tspan class="cc"> -——————————————————————————————————————————-—-</tspan></text></g>
  <g clip-path="url(#lc1)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="66" class="cc">. </tspan><tspan class="key">Subject</tspan><tspan class="cc">: .......................... </tspan><tspan class="value">Khushboo Khator</tspan></text></g>
  <g clip-path="url(#lc2)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="88" class="cc">. </tspan><tspan class="key">Role</tspan><tspan class="cc">: ............................. </tspan><tspan class="value">AI Engineer · Full-Stack Dev</tspan></text></g>
  <g clip-path="url(#lc3)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="110" class="cc">. </tspan><tspan class="key">Origin</tspan><tspan class="cc">: ........................... </tspan><tspan class="value">Gwalior, Madhya Pradesh, India</tspan></text></g>
  <g clip-path="url(#lc4)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="132" class="cc">. </tspan><tspan class="key">Education</tspan><tspan class="cc">: ......................... </tspan><tspan class="value">B.Tech CSE (AI &amp; ML Focus)</tspan></text></g>
  <g clip-path="url(#lc5)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="154" class="cc">. </tspan><tspan class="key">Status</tspan><tspan class="cc">: ............ </tspan><tspan class="value">Building • Learning • Shipping</tspan></text></g>
  <g clip-path="url(#lc6)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="176" class="cc">. </tspan><tspan class="key">ToolChain</tspan><tspan class="cc">: ................. </tspan><tspan class="value">VS Code, Git, Docker, Postman, Vite</tspan></text></g>
  <g clip-path="url(#lc7)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="198" class="cc">. </tspan></text></g>
  <g clip-path="url(#lc8)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="220" class="cc">. </tspan><tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Lang</tspan><tspan class="cc">: .......... </tspan><tspan class="value">Python, TypeScript, JavaScript, SQL</tspan></text></g>
  <g clip-path="url(#lc9)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="242" class="cc">. </tspan><tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Frontend</tspan><tspan class="cc">: ...... </tspan><tspan class="value">React, Next.js, Tailwind CSS, HTML, CSS</tspan></text></g>
  <g clip-path="url(#lc10)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="264" class="cc">. </tspan><tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Backend</tspan><tspan class="cc">: ....... </tspan><tspan class="value">Node.js, Express.js, FastAPI, Hono</tspan></text></g>
  <g clip-path="url(#lc11)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="286" class="cc">. </tspan><tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Database</tspan><tspan class="cc">: ...... </tspan><tspan class="value">PostgreSQL, MongoDB, Prisma, Supabase</tspan></text></g>
  <g clip-path="url(#lc12)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="308" class="cc">. </tspan><tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Infra</tspan><tspan class="cc">: ......... </tspan><tspan class="value">Docker, JWT/RBAC, Vercel</tspan></text></g>
  <g clip-path="url(#lc13)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="330" class="cc">. </tspan></text></g>
  <g clip-path="url(#lc14)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="352" class="accent">- Contact &amp; Work</tspan><tspan class="cc"> -————————————————————————————————————-—-</tspan></text></g>
  <g clip-path="url(#lc15)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="374" class="cc">. </tspan><tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">Mail</tspan><tspan class="cc">: ....................... </tspan><tspan class="value">khushboocodes@gmail.com</tspan></text></g>
  <g clip-path="url(#lc16)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="396" class="cc">. </tspan><tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">Projects</tspan><tspan class="cc">: .................. </tspan><tspan class="value">Nivaran · Recoup · StartupOps</tspan></text></g>
  <g clip-path="url(#lc17)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="418" class="cc">. </tspan><tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">LinkedIn</tspan><tspan class="cc">: .................. </tspan><tspan class="value">khushboo-khator-838aa82a0</tspan></text></g>
  <g clip-path="url(#lc18)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="440" class="cc">. </tspan><tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">Github</tspan><tspan class="cc">: ..................... </tspan><tspan class="value">khushboocodes</tspan></text></g>
  <g clip-path="url(#lc19)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="462" class="cc">. </tspan></text></g>
  <g clip-path="url(#lc20)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="484" class="accent">- Live Stats</tspan><tspan class="cc"> -————————————————————————————————————————————-—-</tspan></text></g>
  <g clip-path="url(#lc21)"><text x="520" y="0" fill="{text_fill}"><tspan x="520" y="506" class="cc">. </tspan><tspan class="value">See live GitHub stats badges below in README ↓</tspan></text></g>

  <rect x="522" y="491.0" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="3.66s" repeatCount="indefinite"/>
  </rect>
</g>

{scan_overlay}

{border_box}
</svg>
"""
    return svg_content

if __name__ == "__main__":
    dark_svg = build_svg(is_dark=True)
    light_svg = build_svg(is_dark=False)
    Path("dark.svg").write_text(dark_svg, encoding="utf-8")
    Path("light.svg").write_text(light_svg, encoding="utf-8")
    print(f"Re-built dark.svg ({len(dark_svg)} bytes) and light.svg ({len(light_svg)} bytes) with verified repository languages.")
