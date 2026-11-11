from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_pro_presentation():
    # ساخت پاورپوینت جدید (ابعاد 16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # ---------------- اسلاید اول: عنوان ----------------
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # اسلاید کاملاً خالی
    
    # ۱. مثلث گوشه بالا-راست (سبز شفاف)
    tri1 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, Inches(9.5), Inches(-1), Inches(5), Inches(5))
    tri1.fill.solid()
    tri1.fill.fore_color.rgb = RGBColor(46, 125, 50) # #2E7D32
    tri1.fill.transparency = 0.4
    tri1.line.fill.background() # بدون حاشیه
    
    # ۲. مثلث گوشه پایین-چپ (سبز شفاف)
    tri2 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, Inches(-1), Inches(4), Inches(4), Inches(4))
    tri2.fill.solid()
    tri2.fill.fore_color.rgb = RGBColor(129, 199, 132) # #81C784
    tri2.fill.transparency = 0.5
    tri2.rotation = 180
    tri2.line.fill.background()
    
    # ۳. کارت سفید وسط (برای قرارگیری متن‌ها)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2), Inches(2), Inches(9.3), Inches(3.5))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.color.rgb = RGBColor(200, 200, 200)
    card.line.width = Pt(1)
    
    # ۴. عنوان (داخل کارت)
    title_box = slide.shapes.add_textbox(Inches(2.5), Inches(2.8), Inches(8.3), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = "تحلیل اکتشافی داده‌ها (EDA)"
    p.font.name = 'B Nazanin'
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(46, 125, 50) # سبز تیره
    p.alignment = PP_ALIGN.CENTER
    
    # ۵. زیرعنوان
    sub_box = slide.shapes.add_textbox(Inches(2.5), Inches(4), Inches(8.3), Inches(1))
    tf2 = sub_box.text_frame
    tf2.word_wrap = True
    p2 = tf2.add_paragraph()
    p2.text = "مطالعه موردی: دیتاست Sample Superstore\nارائه‌دهنده: [نام شما] - استاد: [نام استاد]"
    p2.font.name = 'B Nazanin'
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(85, 85, 85) # خاکستری
    p2.alignment = PP_ALIGN.CENTER
    
    # ---------------- اسلاید دوم: یک نمونه اسلاید محتوا ----------------
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # نوار رنگی بالای اسلاید
    header_bar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.8))
    header_bar.fill.solid()
    header_bar.fill.fore_color.rgb = RGBColor(46, 125, 50)
    header_bar.line.fill.background()
    
    # عنوان اسلاید دوم
    title2 = slide2.shapes.add_textbox(Inches(0.5), Inches(0.1), Inches(10), Inches(0.6))
    p_title2 = title2.text_frame.add_paragraph()
    p_title2.text = "سوال ۱: روند فروش در طول زمان"
    p_title2.font.name = 'B Nazanin'
    p2.font.size = Pt(28)
    p_title2.font.color.rgb = RGBColor(255, 255, 255)
    p_title2.font.bold = True
    
    # متن محتوا (بولت‌پوینت)
    content_box = slide2.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(5), Inches(4))
    tf_content = content_box.text_frame
    tf_content.word_wrap = True
    p_content = tf_content.add_paragraph()
    p_content.text = "یافته‌های کلیدی:"
    p_content.font.name = 'B Nazanin'
    p_content.font.size = Pt(24)
    p_content.font.bold = True
    
    bullets = [
        "روند کلی فروش در ۴ سال صعودی است.",
        "فصلیت قوی در ماه‌های سپتامبر، نوامبر و دسامبر.",
        "بیشترین رشد فروش مربوط به سال ۲۰۱۸ است."
    ]
    for b in bullets:
        p_b = tf_content.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.name = 'B Nazanin'
        p_b.font.size = Pt(20)
        p_b.font.color.rgb = RGBColor(51, 51, 51)
        p_b.space_after = Pt(12)

    # نکته: اینجا می‌توانی با کد، عکس نمودارت را هم اضافه کنی:
    # slide2.shapes.add_picture('path_to_your_chart.png', Inches(6), Inches(1.5), width=Inches(6.5))

    # ذخیره فایل
    prs.save('Superstore_Professional_Presentation.pptx')
    print("پاورپوینت با موفقیت ساخته شد!")

# اجرای تابع
create_pro_presentation()