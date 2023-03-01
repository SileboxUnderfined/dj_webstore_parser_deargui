import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Hello, World!', width=600, height=300)

with dpg.window(label='Example window'):
    dpg.add_text("Hello, World")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()