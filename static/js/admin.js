

app = new Vue({
    el: '#app',
    data: {
        max_individual_songs: 3,
        max_downvotes: 3,
        safe_mode: false
    },
    watch: {
        max_downvotes: function () {
            $.post('/options', {max_downvotes: this.max_downvotes}).done(
                function (data) {console.log(data)}
            )
        },
        max_individual_songs: function () {
            $.post('/options', {max_individual_songs: this.max_individual_songs}).done(
                function (data) {console.log(data)}
            )
        },
        safe_mode: function () {
            $.post('/options', {safe_mode: this.safe_mode}).done(
                function (data) {console.log(data)}
            )
        }
    }
})

$.get('/options').done(function (data) {
    data = JSON.parse(data)
    app.max_individual_songs = data.max_individual_songs
    app.max_downvotes = data.max_downvotes
    app.safe_mode = data.safe_mode
})