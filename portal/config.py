class UrlConfig:
    home_url = "http://www.njau.edu.cn/"

    portal_url = "https://authserver.njau.edu.cn/"
    portal_index_url = "http://myportal.njau.edu.cn/"
    portal_login_url = portal_url + "authserver/login"
    portal_user_url = portal_index_url + "jsonp/userDesktopInfo.json?type=&_=%d"
    portal_login_service_url = portal_index_url + "login?service=http://myportal.njau.edu.cn/new"
    portal_check_captcha_url = portal_url + "authserver/checkNeedCaptcha.htl"
    portal_captcha_url = portal_url + "authserver/getCaptcha.htl"

    # 教务处链接
    jw_url = "http://jw1.njau.edu.cn/jsxsd/"
    jw_framework_url = jw_url + "framework/"
    jw_xskb_url = jw_url + "xskb"
    jw_xsks_url = jw_url + "xsks"
    jw_pyfa_url = jw_url + "pyfa"
    jw_user_url = jw_framework_url + "xsMain.jsp"
    jw_course_schedule_url = jw_url + "xskb/xskb_list.do"
    jw_course_list_url = jw_url + "xskb/xskb_list_new.do"
    jw_lesson_detail_url = jw_url + "xskb/queryDetails.do"
    jw_grade_kscj_url = jw_url + "kscj/"
    jw_grade_total_url = jw_grade_kscj_url + "sxcjcx_list"
    jw_grade_archive_url = jw_grade_kscj_url + "gdcjcx_list"
    jw_grade_current_url = jw_grade_kscj_url + "dxqcjcx_list"
    jw_grade_level_url = jw_grade_kscj_url + "djkscj_list"
    jw_class_contact_url = jw_xskb_url + "/sksm_list.do"
    jw_class_contact_detail_url = jw_xskb_url + "/showTzdLxfs.do?jx0404id="
    jw_exam_index_url = jw_xsks_url + "/xsksap_query"
    jw_exam_detail_url = jw_xsks_url + "/xsksap_list"
    jw_credit_innovation_url = jw_pyfa_url + "/cxxf_query"
    jw_credit_application_url = jw_pyfa_url + "/cxxfsb_query"
    jw_credit_usage_url = jw_pyfa_url + "/cxxfsy_query"
