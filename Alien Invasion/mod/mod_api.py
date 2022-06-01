class ModApi():
    def __init__(self, settings):
        self.settings = settings

    def mod_bullet(self, speed, width, height, color, allowed):
        self.settings.bullet_speed_factor = speed
        self.settings.bullet_width = width
        self.settings.bullet_height = height
        self.settings.bullet_color = color
        self.settings.bullets_allowed = allowed

    def js_print(self, msg):
        print(msg)