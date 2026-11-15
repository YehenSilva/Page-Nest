import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_gradient(width, height, top_color, bot_color):
    base = Image.new('RGBA', (width, height), top_color)
    top_r, top_g, top_b = top_color[:3]
    bot_r, bot_g, bot_b = bot_color[:3]
    for y in range(height):
        ratio = y / float(height)
        r = int(top_r + (bot_r - top_r) * ratio)
        g = int(top_g + (bot_g - top_g) * ratio)
        b = int(top_b + (bot_b - top_b) * ratio)
        line = Image.new('RGBA', (width, 1), (r, g, b, 255))
        base.paste(line, (0, y))
    return base

def draw_radial_glow(img, cx, cy, radius, color, max_alpha):
    glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    r, g, b = color[:3]
    steps = 40
    for i in range(steps, 0, -1):
        rad = radius * (i / steps)
        alpha = int(max_alpha * (1 - i / steps) ** 1.5)
        bbox = [cx - rad, cy - rad, cx + rad, cy + rad]
        draw.ellipse(bbox, fill=(r, g, b, alpha))
    img.alpha_composite(glow)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def main():
    W, H = 2400, 1260
    os.makedirs('assets', exist_ok=True)
    os.makedirs('scripts', exist_ok=True)

    print("Creating canvas...")
    canvas = make_gradient(W, H, (10, 11, 16), (15, 17, 24))

    # Ambient Glows
    print("Adding ambient lighting...")
    draw_radial_glow(canvas, 1200, 680, 950, (99, 102, 241), 40)   # Indigo under window
    draw_radial_glow(canvas, 450, 260, 500, (56, 189, 248), 24)    # Sky accent top-left
    draw_radial_glow(canvas, 1950, 320, 600, (168, 85, 247), 28)  # Purple accent top-right

    # Grid lines
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    grid_spacing = 48
    for x in range(0, W, grid_spacing):
        gdraw.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, H, grid_spacing):
        gdraw.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)
    canvas.alpha_composite(grid)

    # Load system fonts
    font_brand = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)
    font_h1 = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 56)
    font_sub = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 23)
    font_pill = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 16)
    font_wtitle = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 15)
    font_card_tag = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 14)

    draw = ImageDraw.Draw(canvas)

    # 1. Top Brand Pill
    pill_text = "PageNest v2.0  •  Zero-Cost Knowledge Workspace"
    bbox_pill = font_brand.getbbox(pill_text)
    pw = (bbox_pill[2] - bbox_pill[0]) + 52
    ph = 38
    px0 = (W - pw) // 2
    py0 = 55
    draw_rounded_rect(draw, [px0, py0, px0 + pw, py0 + ph], radius=19,
                      fill=(255, 255, 255, 14), outline=(255, 255, 255, 36), width=1)

    # Brand icon indicator
    draw.ellipse([px0 + 16, py0 + 14, px0 + 26, py0 + 24], fill=(99, 102, 241, 240))
    draw.text((px0 + 38, py0 + 8), pill_text, fill=(226, 232, 240, 255), font=font_brand)

    # 2. Main Headline
    h1_text = "Structure, Connect & Collaborate."
    h1_bbox = font_h1.getbbox(h1_text)
    h1_w = h1_bbox[2] - h1_bbox[0]
    draw.text(((W - h1_w) // 2, 115), h1_text, fill=(255, 255, 255, 255), font=font_h1)

    # 3. Subtitle
    sub_text = "The minimalist, Notion-grade knowledge workspace built natively on Firebase Spark."
    sub_bbox = font_sub.getbbox(sub_text)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((W - sub_w) // 2, 195), sub_text, fill=(148, 163, 184, 255), font=font_sub)

    # 4. Feature Badges Row
    badges = [
        "⚡ Real-time Sync",
        "📋 17 Block Types & Tables",
        "⌨️ Command Palette (Ctrl+K)",
        "📁 Nestable Pages & Favorites",
        "💸 $0/mo Spark Tier"
    ]
    total_badges_w = 0
    badge_widths = []
    for b in badges:
        bb = font_pill.getbbox(b)
        bw = (bb[2] - bb[0]) + 30
        badge_widths.append(bw)
        total_badges_w += bw
    total_badges_w += (len(badges) - 1) * 12

    cur_bx = (W - total_badges_w) // 2
    by0 = 248
    bh = 32
    for b, bw in zip(badges, badge_widths):
        draw_rounded_rect(draw, [cur_bx, by0, cur_bx + bw, by0 + bh], radius=16,
                          fill=(255, 255, 255, 10), outline=(255, 255, 255, 24), width=1)
        bb = font_pill.getbbox(b)
        tw = bb[2] - bb[0]
        draw.text((cur_bx + (bw - tw) // 2, by0 + 6), b, fill=(203, 213, 225, 240), font=font_pill)
        cur_bx += bw + 12

    # 5. Application Window Showcase
    print("Composing application window mockup...")
    win_w = 2040
    win_h = 1000
    win_x = (W - win_w) // 2
    win_y = 310

    # Multi-layered window shadow
    shadow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    # Deep shadow
    draw_rounded_rect(sdraw, [win_x - 10, win_y + 15, win_x + win_w + 10, win_y + win_h + 30],
                      radius=24, fill=(0, 0, 0, 180))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(38))
    canvas.alpha_composite(shadow_layer)

    # Window container
    window_img = Image.new('RGBA', (win_w, win_h), (24, 24, 27, 255))
    wdraw = ImageDraw.Draw(window_img)

    # Titlebar
    tb_h = 46
    wdraw.rectangle([0, 0, win_w, tb_h], fill=(24, 24, 27, 255))
    wdraw.line([(0, tb_h), (win_w, tb_h)], fill=(45, 45, 48, 255), width=1)

    # macOS traffic lights
    dot_y = 23
    wdraw.ellipse([22, dot_y - 6, 34, dot_y + 6], fill=(255, 95, 86, 255))   # Red
    wdraw.ellipse([42, dot_y - 6, 54, dot_y + 6], fill=(255, 189, 46, 255))  # Yellow
    wdraw.ellipse([62, dot_y - 6, 74, dot_y + 6], fill=(39, 201, 63, 255))   # Green

    # Window title & breadcrumb
    wtitle_text = "PageNest  —  Product Vision & Roadmap 2026"
    wt_bbox = font_wtitle.getbbox(wtitle_text)
    wt_w = wt_bbox[2] - wt_bbox[0]
    wdraw.text(((win_w - wt_w) // 2, 14), wtitle_text, fill=(161, 161, 170, 255), font=font_wtitle)

    # Window Body - Load the genuine Retina screenshot!
    retina_path = 'assets/app_screenshot_retina.png'
    if os.path.exists(retina_path):
        app_shot = Image.open(retina_path)
        # Scale to match win_w exactly
        scale = win_w / float(app_shot.width)
        scaled_h = int(app_shot.height * scale)
        app_shot_resized = app_shot.resize((win_w, scaled_h), Image.Resampling.LANCZOS)
        
        # Paste into window body under titlebar
        window_img.paste(app_shot_resized, (0, tb_h))
    else:
        print("Warning: retina screenshot not found!")

    # Round the window corners
    mask = Image.new('L', (win_w, win_h), 0)
    mdraw = ImageDraw.Draw(mask)
    draw_rounded_rect(mdraw, [0, 0, win_w, win_h], radius=20, fill=255)

    # Border around the window
    border_layer = Image.new('RGBA', (win_w, win_h), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_layer)
    draw_rounded_rect(bdraw, [0, 0, win_w - 1, win_h - 1], radius=20, outline=(255, 255, 255, 38), width=1)

    canvas.paste(window_img, (win_x, win_y), mask)
    canvas.paste(border_layer, (win_x, win_y), mask)

    # 6. Floating Command Palette Showcase Card (Bottom Right)
    cmd_crop_path = 'assets/cmd_palette_crop.png'
    if os.path.exists(cmd_crop_path):
        print("Adding floating Command Palette showcase...")
        card_w = 640
        card_h = 420
        card_x = win_x + win_w - card_w - 50
        card_y = win_y + win_h - card_h - 60

        # Card shadow
        card_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        csdraw = ImageDraw.Draw(card_shadow)
        draw_rounded_rect(csdraw, [card_x - 6, card_y + 8, card_x + card_w + 6, card_y + card_h + 16],
                          radius=20, fill=(0, 0, 0, 210))
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(28))
        canvas.alpha_composite(card_shadow)

        # Card Container
        card_img = Image.new('RGBA', (card_w, card_h), (20, 20, 23, 255))
        cdraw = ImageDraw.Draw(card_img)

        # Header bar of card
        cdraw.rectangle([0, 0, card_w, 38], fill=(28, 28, 32, 255))
        cdraw.line([(0, 38), (card_w, 38)], fill=(45, 45, 48, 255), width=1)
        cdraw.text((16, 11), "⚡ Command Palette & Fuzzy Search", fill=(199, 210, 254, 255), font=font_card_tag)

        # Paste cropped command palette image
        cmd_img = Image.open(cmd_crop_path)
        cmd_scaled = cmd_img.resize((card_w, card_h - 38), Image.Resampling.LANCZOS)
        card_img.paste(cmd_scaled, (0, 38))

        # Card mask & border
        cmask = Image.new('L', (card_w, card_h), 0)
        cmdraw = ImageDraw.Draw(cmask)
        draw_rounded_rect(cmdraw, [0, 0, card_w, card_h], radius=16, fill=255)

        cborder = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0))
        cbdraw = ImageDraw.Draw(cborder)
        draw_rounded_rect(cbdraw, [0, 0, card_w - 1, card_h - 1], radius=16,
                          outline=(129, 140, 248, 120), width=1)

        canvas.paste(card_img, (card_x, card_y), cmask)
        canvas.paste(cborder, (card_x, card_y), cmask)

    # Save outputs
    out_png = 'assets/banner.png'
    canvas.save(out_png, 'PNG', optimize=True)
    print(f"Saved {out_png} ({os.path.getsize(out_png)} bytes)")

    # Also generate assets/banner.svg with embedded high-res screenshot
    import base64
    with open(out_png, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    out_svg = 'assets/banner.svg'
    with open(out_svg, 'w', encoding='utf-8') as f:
        f.write(f'''<svg width="2400" height="1260" viewBox="0 0 2400 1260" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <image width="2400" height="1260" href="data:image/png;base64,{b64}"/>
</svg>''')
    print(f"Saved {out_svg} ({os.path.getsize(out_svg)} bytes)")

if __name__ == '__main__':
    main()
