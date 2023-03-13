import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Parser!', width=400, height=200, resizable=False)

with dpg.font_registry():
    with dpg.font('Ubuntu-Medium.ttf',13,default_font=True, id='default_font'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    dpg.bind_font('default_font')

with dpg.window(width=400, height=200, tag='Parser Selector'):
    dpg.add_text("Выберите парсер:")
    dpg.add_button(label='dj_webstore')
    dpg.add_button(label='dex_de')
    dpg.add


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Parser Selector', True)
dpg.start_dearpygui()
dpg.destroy_context()