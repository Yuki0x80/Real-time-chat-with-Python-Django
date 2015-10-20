define(["backbone", "underscore", "text!templates/message.tmpl"], function(e, t, n) {
    return e.View.extend({
        tagName: "div",
        className: "monologue",
        template: t.template(n),
        render: function() {
            return this.$el.html(this.template(this.model.toJSON())), this
        }
    })
});