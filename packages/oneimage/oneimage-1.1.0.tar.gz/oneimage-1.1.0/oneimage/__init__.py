# -*- coding: UTF-8 -*
'''
Created on 2020-08-10
'''
from __future__ import print_function

__version__ = '1.1.0'


def _md5(s):
    import hashlib
    m2 = hashlib.md5()
    m2.update(s.encode("utf8"))
    return m2.hexdigest()


def get_cached_file(url):
    import os
    cachepath = os.path.join('cache')
    if not os.path.exists(cachepath):
        os.makedirs(cachepath)
    fn = url[url.rfind('/'):]
    if '.' in fn:
        suffix = fn[fn.rfind('.'):]
        if '?' in suffix:
            suffix = suffix[0:suffix.index('suffix')]
    else:
        suffix = ''
    filepath = os.path.join(cachepath, _md5(url) + suffix)
    if not os.path.exists(filepath):
        import requests
        content = requests.get(url).content
        with open(filepath, 'wb') as f:
            f.write(content)
    return filepath


def create_image(data, file_getter=None, debug=False):
    try:
        import Image, ImageDraw, ImageFont, ImageFilter
    except:
        pass
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
    except:
        pass
    try:
        # py2
        from StringIO import StringIO
    except:
        # py3
        from io import BytesIO as StringIO

    if not file_getter:
        file_getter = get_cached_file

    def get_img_with_width(url, width=0, height=0, mode='fill'):
        bgpath = file_getter(url)
        if not bgpath:
            return
        img = Image.open(bgpath)
        (bw, bh) = img.size
        if mode == 'fit' and width and height and bw and bh:
            # 等比例缩放
            ss = float(bw) / bh
            ds = float(width) / height
            if ss > ds:
                # 太宽
                nw = int(bh * ds)
                ow = (bw - nw) / 2
                img = img.crop((ow, 0, bw - ow, bh), )
                bw = nw
            elif ds > ss:
                # 太高
                nh = int(bw / ds)
                oh = (bh - nh) / 2
                img = img.crop((0, oh, bw, bh - oh), )
                bh = nh
        if width and bw != width:
            if not height:
                height = int(float(bh) * float(width) / float(bw))
            img = img.resize((width, height), Image.ANTIALIAS)
        return img

    def get_truetype_font_with_size(url, size=10):
        path = file_getter(url)
        font = ImageFont.truetype(path, size)
        return font

    def get_lines_with_draw_font(draw, font, text, spacing, width=0, height=0):
        lns = []
        if width or height:
            totalh = 0
            totalw = 0
            for ln in text.split('\n'):
                ts = []
                pw, ph = 0, 0
                for i in range(len(ln)):
                    tt = ''.join(ts) + ln[i]
                    tw, th = draw.textsize(tt, spacing=spacing, font=font)
                    if width and ts and tw >= width:
                        # full
                        lns.append((pw, ph, ''.join(ts)), )
                        totalw = max(totalw, pw)
                        totalh += th
                        del ts[:]
                    ts.append(ln[i])
                    pw, ph = tw, th
                    if height and (totalh + th) >= height:
                        break
                if ts and (totalh < height or not height):
                    tw, th = draw.textsize(tt, spacing=spacing, font=font)
                    if not height or (th + totalh) <= height:
                        lns.append((tw, th, ''.join(ts)), )
                        totalw = max(totalw, tw)
                        totalh += th
                    del ts[:]
                if height and totalh >= height:
                    break
        else:
            totalw, totalh = draw.multiline_textsize(text, spacing=spacing, font=font)
            lns.append((totalw, totalh, text), )
        return totalw, totalh, lns

    width = data['width']
    height = data['height']
    img = Image.new("RGBA", (width, height), data.get('background', (255, 255, 255, 0)))
    draw = ImageDraw.Draw(img)
    elements = data['elements']

    def _add_corners(im, rad=100):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    for ele in elements:
        if ele.get('type') == 'image':
            imgd = ele
            if not imgd.get('url'):
                continue
            try:
                im = get_img_with_width(imgd['url'], width=imgd.get('width', width), height=imgd.get('height', 0), mode=imgd.get('mode', 'fill'))
            except:
                import traceback
                traceback.print_exc()
                im = None
            if not im:
                continue
            if im.mode not in ['RGBA']:
                im = im.convert('RGBA')
            radius = imgd.get('radius')
            if imgd.get('rotate'):
                im = im.rotate(imgd['rotate'])
            if radius:
                im = _add_corners(im, radius)
                _, _, _, mask = im.split()
            elif im.mode == 'RGBA':
                _, _, _, mask = im.split()
            else:
                mask = None
            tl = int(imgd.get('left', 0))
            tt = int(imgd.get('top', 0))
            tw, th = im.size
            img.paste(im, (tl, tt), mask=mask)
        elif ele.get('type') == 'text':
            txtd = ele
            size = txtd['size']
            font = get_truetype_font_with_size(txtd['font'], size)
            # if not font:
            #     continue
            text = txtd['text']
            if not text:
                continue
            left = txtd.get('left', 0)
            top = txtd.get('top', 0)
            spacing = int(txtd.get('spacing', 4))
            width = txtd.get('width') or 0
            height = txtd.get('height') or 0
            fw, fh, lns = get_lines_with_draw_font(draw=draw, font=font, text=text, spacing=spacing, width=width, height=height)
            tw = max(fw, width)
            th = max(fh, height)
            tl = left
            tt = top
            if txtd.get('background'):
                # 背景色
                pd = txtd.get('padding', 0)
                pl = txtd.get('padding-left', pd)
                pr = txtd.get('padding-right', pd)
                pt = txtd.get('padding-top', pd)
                pb = txtd.get('padding-bottom', pd)
                tw = tw + pl + pr
                th = th + pt + pb
                bg = Image.new("RGBA", (tw, th), txtd.get('background'))
                radius = txtd.get('radius')
                if radius:
                    bg = _add_corners(bg, radius)
                    _, _, _, mask = bg.split()
                else:
                    mask = None
                tl = left - pl
                tt = top - pt
                img.paste(bg, (tl, tt), mask=mask)
            align = txtd.get('align', 'center')  # 水平方向
            valign = txtd.get('vertical', 'top')  # 水平方向
            if valign == 'center':
                ih = int((height - fh) / 2)
            elif valign == 'bottom':
                ih = int(height - fh)
            else:
                ih = 0
            for w, h, txt in lns:
                l = left
                t = top + ih
                if width:
                    if align == 'center':
                        l += int((width - w) / 2)
                    elif align == 'right':
                        l = l + width - w
                draw.text((l, t), txt, font=font, spacing=spacing, fill=txtd.get('color', 'black'))
                ih += h

            # 绘制文字
            if txtd.get('line-through'):
                width = int(txtd.get('line-through', '1'))
                draw.line([(tl, tt + th / 2 + width / 4), (tl + tw, tt + th / 2 + width / 4)], width=width, fill=txtd.get('color'))
        if debug:
            draw.line([(tl, tt), (tl + tw - 1, tt), (tl + tw - 1, tt + th - 1), (tl, tt + th - 1), (tl, tt)], width=1, fill=debug)
    return img
