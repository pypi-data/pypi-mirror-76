import os

from pptx_tools.creator import PPTXCreator, PPTXPosition
from pptx_tools.font_style import PPTXFontStyle
from pptx_tools.style_sheets import font_title, font_default
from pptx_tools.templates import TemplateExample

from pptx.enum.lang import MSO_LANGUAGE_ID
from pptx.enum.text import MSO_TEXT_UNDERLINE_TYPE

try:
    import matplotlib.pyplot as plt
    matplotlib_installed = True
except ImportError as e:
    matplotlib_installed = False

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def run(save_dir: str):
    pp = PPTXCreator(TemplateExample())

    PPTXFontStyle.lanaguage_id = MSO_LANGUAGE_ID.ENGLISH_UK
    PPTXFontStyle.name = "Roboto"

    title_slide = pp.add_title_slide("Equation presentation")
    font = font_title()  # returns a PPTXFontStyle instance with bold font and size = 32 Pt
    font.write_shape(title_slide.shapes.title)  # change font attributes for all paragraphs in shape

#    pp.add_latex_formula(f"\mu={5}^{5}", title_slide, PPTXPosition(0.75, 0.35))
    formula01 = "E_{r} = \\frac{1}{2} \sqrt{\\frac{\pi}{A}} \\frac{\mathrm{d}P}{\mathrm{d}h}"
    formula02 = "E_{r} = \\frac{1-\\nu_i^2}{E_i} + \\frac{1-\\nu^2}{E}"
    formula03 = "E_{r} = \\frac{1}{2} \\frac{1}{\\beta} \sqrt{\\frac{\pi}{A}} \\frac{\mathrm{d}P}{\mathrm{d}h}"
    formula04 = "\epsilon = \\frac{\sigma}{E} + K \left(\\frac{\sigma}{E}\\right)^n"
    pp.add_latex_formula(formula01, title_slide, PPTXPosition(0.25, 0.35))
    pp.add_latex_formula(formula02, title_slide, PPTXPosition(0.25, 0.45))
    pp.add_latex_formula(formula03, title_slide, PPTXPosition(0.25, 0.55))
    pp.add_latex_formula(formula04, title_slide, PPTXPosition(0.25, 0.65))

    pp.save(os.path.join(save_dir, "equations2.pptx"))


if __name__ == '__main__':
    save_dir = os.path.dirname(os.path.abspath(__file__)) + '\\output\\'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    run(save_dir)