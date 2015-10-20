define(["backbone", "channel"], function(e, t) {
    return e.View.extend({
        el: ".input-area",
        events: {
            "click .submit": "submit",
            "keypress textarea": "submitOnEnter"
        },
        submit: function() {
            nwmsg = this.$el.find("textarea").val(), this.$el.find("textarea").val(""), t.trigger("addMsg", nwmsg)
            console.log(nwmsg)
        },
        submitOnEnter: function(e) {
            console.log(e.keyCode), e.keyCode === 13 && !e.shiftKey && this.submit()
        }
    })
});