#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under the WTFPL license, http://sam.zoy.org/wtfpl/.

import cairo
import pango
import pangocairo
import os.path
import sys
import optparse
from qrcodes import download_qr_code
__version__ = '0.1'

BADGE_HEIGHT = 148.5
BADGE_WIDTH  = 105

PAGE_HEIGHT = 297
PAGE_WIDTH = 210

INNER_MARGIN = 0

TEXT_COLOR = (0.2, 0.2, 0.2)
TEXT_COLOR_ROLE = (1, 1, 1)

def convert_mm_to_dots(mm):
    return float(mm) / 25.4 * 72

def draw_text(ctx, pc, text, base_font_sz, y, text_width, text_height,
              area_width, multiline=False):
    font_sz = base_font_sz
    while font_sz > 6:
        name_fd = pango.FontDescription("Product Sans")
        name_fd.set_size(font_sz * pango.SCALE)
        layout = pc.create_layout()
        layout.set_font_description(name_fd)
        layout.set_text(text)
        layout.set_alignment(pango.ALIGN_CENTER)
        if multiline:
            layout.set_width(int(convert_mm_to_dots(text_width) * pango.SCALE))

        if layout.get_size()[0] > (convert_mm_to_dots(text_width) * pango.SCALE):
            font_sz -= 1
            continue

        if layout.get_size()[1] > (convert_mm_to_dots(text_height) * pango.SCALE):
            font_sz -= 1
            continue

        # draw
        text_x, text_y, text_w, text_h = layout.get_extents()[1]
        x = (convert_mm_to_dots(area_width) / 2) - (text_w/2.0)/pango.SCALE - int(float(text_x)/pango.SCALE)
        y = y + (convert_mm_to_dots(text_height)/2) - (text_h/2.0)/pango.SCALE - int(float(text_y)/pango.SCALE)
        ctx.move_to(x, y)
        pc.show_layout(layout)
        break


def draw_badge(ctx, width, height, description, background_image, qrcodes_directory, id=0):
    im = cairo.ImageSurface.create_from_png(background_image)

    ctx.save()
    ctx.rectangle(0, 0, convert_mm_to_dots(width),
                  convert_mm_to_dots(height))
    ctx.scale(float(convert_mm_to_dots(width)) / im.get_width(),
              float(convert_mm_to_dots(height)) / im.get_height())
    ctx.set_source_surface(im)
    ctx.fill()


    if len(description) == 0:
        return

    if len(description) > 3:
        role = description[3].strip()
    else:
        role = ''
    
    if len(description) > 6:
        id = description[6].strip()


    # -- QRCODE --
    file_path = qrcodes_directory + "/qrcode_" + str(id) + ".png"

    im = cairo.ImageSurface.create_from_png(file_path)
    
    width_offset = 910
    height_offset = 1420
    
    ctx.rectangle(0,0, 1400,1800)
    ctx.translate(width_offset, height_offset)
    ctx.scale(0.7, 0.7)
    ctx.set_source_surface(im)
    ctx.fill()
    # -- END QRCODE --


    ctx.restore()

    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.rectangle(0, 0, convert_mm_to_dots(width),
                  convert_mm_to_dots(height))
    ctx.stroke()



def generate_document(input_csv, output_pdf, background_image, qrcodes_directory):
    surface = cairo.PDFSurface(output_pdf,
                               convert_mm_to_dots(PAGE_WIDTH),
                               convert_mm_to_dots(PAGE_HEIGHT))

    nb_badges_height = PAGE_HEIGHT / (BADGE_HEIGHT + INNER_MARGIN)
    nb_badges_width  = PAGE_WIDTH / (BADGE_WIDTH + INNER_MARGIN)

    margin_top_bottom = (PAGE_HEIGHT - \
                             nb_badges_height * BADGE_HEIGHT - \
                             (nb_badges_height - 1) * INNER_MARGIN) / 2

    margin_left_right = (PAGE_WIDTH - \
                             nb_badges_width * BADGE_WIDTH - \
                             (nb_badges_width - 1) * INNER_MARGIN) / 2

    import csv
    csvFile = csv.reader(open(input_csv, 'rb'), delimiter=',')

    ctx = cairo.Context(surface)

    row = 0
    col = 0

    badges = list(csvFile)
    nb_badges = len(badges)

    for index in range(nb_badges):
        # Reverse the badge order for printing issues.
        if(index%2 == 0):
           badge_back = badges[index + 1]
        else:
            badge_back = badges[index-1]


        ctx.save()
        ctx.translate(convert_mm_to_dots(margin_left_right + col * (BADGE_WIDTH + INNER_MARGIN)),
                      convert_mm_to_dots(margin_top_bottom + row * (BADGE_HEIGHT + INNER_MARGIN)))
        draw_badge(ctx, BADGE_WIDTH, BADGE_HEIGHT, badge_back, background_image, qrcodes_directory, index)
        ctx.restore()

        col += 1
        if col == nb_badges_width:
            col = 0
            row += 1
        if row == nb_badges_height:
            col = 0
            row = 0
            surface.show_page()

    surface.finish()


def download_qr_codes(input_csv):
    import csv
    csvFile = csv.reader(open(input_csv, 'rb'), delimiter=',')

    badges = list(csvFile)
    for index, badge in enumerate(badges):
        # Reverse the badge order for printing issues.
        if(index%2 == 0):
           badge_back = badges[index + 1]
        else:
            badge_back = badges[index-1]


def main():
    usage = '%prog -o output-pdf -i input-csv -b background-image'
    parser = optparse.OptionParser(usage=usage,
                                   version='%%prog %s' % __version__)
    parser.add_option('-o', dest='output_pdf', metavar='OUTPUT_PDF',
                      help='specify the location of the output PDF.')
    parser.add_option('-i', dest='input_csv', metavar='INPUT_CSV',
                      help='specify the location of the input CSV.')
    parser.add_option('-b', dest='background_image', metavar='BACKGROUND_IMAGE',
                      help='specify the location of the background image.')
    parser.add_option('-q', dest='qrcodes_directory', metavar='QRCODES_DIRECTORY',
                       help='specify the location of the qr codes image.')
    

    (options, args) = parser.parse_args()
    if len(args):
        parser.print_help()
        return 1

    if not options.output_pdf:
        parser.error("Missing output PDF")

    if not options.input_csv:
        parser.error("Missing input CSV")
    if not os.path.exists(options.input_csv):
        parser.error("Input CSV %s does not exist" % options.input_csv)

    if not options.background_image:
        parser.error("Missing background image")
    if not os.path.exists(options.background_image):
        parser.error("Background image %s does not exist" % options.background_image)

    if not options.qrcodes_directory:
        parser.error("Missing qr_codes directory")
    if not os.path.exists(options.qrcodes_directory):
        parser.error("QR codes directory %s does not exist" % options.qrcodes_directory)
   
    generate_document(options.input_csv, options.output_pdf, options.background_image, options.qrcodes_directory)



if __name__ == '__main__':
    sys.exit(main())
