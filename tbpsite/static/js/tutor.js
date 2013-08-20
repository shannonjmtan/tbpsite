function getObjectCss() {
	var e = null;
	try {
		var t = document.getElementsByTagName("head").item(0);
		t.appendChild(document.createElement("style")), e = document.styleSheets[document.styleSheets.length - 1]
	} catch (n) {
		e = document.createStyleSheet("tutoringStyle.css")
	}
	return e
}
function addCssRule(e, t, n) {
	e.insertRule ? e.insertRule(t + " { " + n + " }", e.cssRules.length) : e.addRule && e.addRule(t, n)
}
function deleteCssRule(e, t) {
	if (!t) return;
	if (tutoringcss.cssRules) rules = tutoringcss.cssRules;
	else {
		if (!tutoringcss.rules) return;
		rules = tutoringcss.rules
	}
	for (var n = 0; n < rules.length; n++) if (rules[n].selectorText.toLowerCase() == t.toLowerCase()) {
		tutoringcss.deleteRule ? tutoringcss.deleteRule(n) : tutoringcss.removeRule && tutoringcss.removeRule(n);
		return
	}
}
function highlight(e) {
	locked || (deleteCssRule(tutoringcss, "." + highlighted + "_2"), deleteCssRule(tutoringcss, "." + highlighted + "_1"), deleteCssRule(tutoringcss, "." + highlighted + "_0"), highlighted = e, addCssRule(tutoringcss, "." + e + "_2", "background: " + pref_color + " !important"), addCssRule(tutoringcss, "." + e + "_1", "background: " + comp_color + " !important"), addCssRule(tutoringcss, "." + e + "_0", "background: " + curr_color + " !important"))
}
function unhighlight(e) {
	locked || (deleteCssRule(tutoringcss, "." + highlighted + "_2"), deleteCssRule(tutoringcss, "." + highlighted + "_1"), deleteCssRule(tutoringcss, "." + highlighted + "_0"), highlighted = !1)
}
function locklight(e) {
	return locked ? locked != e ? (locked = !1, highlight(e), locked = e) : (locked = !1, highlight(e)) : (highlight(e), locked = e), !1
}
var pref_color = "#3f3",
	comp_color = "#39f",
	curr_color = "#fc0",
	locked = !1,
	highlighted = !1;
$(document).ready(function() {
	$(".tutorbox").hide(), $(".person").hover(function() {
		box = $("#box" + $(this).attr("id")), box.show(), box.css("left", $(this).offset().left + 20), box.css("top", $(this).offset().top + 20)
	}, function() {
		box = $("#box" + $(this).attr("id")), box.hide()
	})
});
var tutoringcss = getObjectCss();
addCssRule(tutoringcss, ".pref", "background: " + pref_color + " !important"), addCssRule(tutoringcss, ".comp", "background: " + comp_color + " !important"), addCssRule(tutoringcss, ".curr", "background: " + curr_color + " !important");
