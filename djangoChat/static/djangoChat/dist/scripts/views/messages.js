define(["backbone", "views/message", "channel"], function(e, t, n) {
    return Messages = e.View.extend({
        tagName: "div",
        className: "chatMsgs",
        initialize: function() {
            this.collection.fetch(), $(".chatBox").html(this.el), this.collection.on("add", this.addOne, this), n.on("addMsg", this.addMsg, this)
        },
        addOne: function(e) {
            var n = new t({
                model: e
            });
            this.$el.append(n.render().el), $("html, body").animate({
                scrollTop: $(document).height()
            }, 300)
        },
        addMsg: function(e) {
            this.collection.create({
                msg: e
            }, {
                wait: !0
            })
        }
    }), Messages
});