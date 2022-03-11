class UrlConfig:
    home_url = "http://www.njau.edu.cn/"

    portal_url = "https://authserver.njau.edu.cn/"
    portal_index_url = "http://myportal.njau.edu.cn/"
    portal_login_url = portal_url + "authserver/login"
    portal_user_url = portal_index_url + "jsonp/userDesktopInfo.json?type=&_=%d"
    portal_login_service_url = portal_index_url + "login?service=http://myportal.njau.edu.cn/new"
    portal_check_captcha_url = portal_url + "authserver/checkNeedCaptcha.htl"
    portal_captcha_url = portal_url + "authserver/getCaptcha.htl"
