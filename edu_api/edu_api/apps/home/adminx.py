import xadmin
from xadmin import views

from home.models import Banner, Nav


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "百知教育"
    site_footer = "北京百知教育科技有限公司"
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSettings)



class BannerInfo(object):
    list_display = ["title", "orders", "is_show"]


xadmin.site.register(Banner, BannerInfo)


class NavInfo(object):
    list_display = ["title", "orders", "is_show"]


xadmin.site.register(Nav, NavInfo)
