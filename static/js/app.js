
socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('client_connected', {data: 'I\'m connected!'});
});

socket.on('queue_changed', function(data) {
    console.log('the queue is updating')
    for (i = 0; i < data.length; i ++) {
        song = data[i]
        song['was_upvoted'] = false;
        song['was_downvoted'] = false;
    }
    app.queue = data;
});

socket.on('suggestions_changed', function(data) {
    console.log('new suggestions inbound');
    app.suggestions = data;
});

socket.on('currently_playing_changed', function (data) {
    console.log('next song')
    data['curr_time'] = 0
    app.currently_playing = data
})



submit_song_url = '/add_song?song=spotify:track:'

Vue.use(VueTouch, {name: 'v-touch'})

app = new Vue({
    el: '#app',
    data: {
        queue: [],
        search: '',
        suggestions: [],
        currently_playing: {
            album_name: '',
            album_uri: '',
            name: '',
            artist: '',
            duration: '',
        }
    },
    watch: {
        search: function () {
            socket.emit('searchbar_changed', {query: this.search})
        }
    },
    methods: {
        submit_song: function (track_id) {
            console.log('submitting...')
            $.ajax(submit_song_url + track_id).done(function (data) {
                console.log('success')
                app.search = ''
            }).fail(function (data) {
                console.log('failure')
            })
        },
        upvote: function (index) {
            song = this.queue[index]
            console.log(song)
            if (song['was_upvoted']) {
                song['was_upvoted'] = false
            }
            else {
                song['was_upvoted'] = true
                song['was_downvoted'] = false
            }
        },
        downvote: function (index) {
            song = this.queue[index]
            console.log(song)
            if (song['was_downvoted']) {
                song['was_downvoted'] = false
            }
            else {
                song['was_downvoted'] = true
                song['was_upvoted'] = false
            }
        }
    }
});


update_progress_bar = function () {
    if (app.currently_playing.curr_time < app.currently_playing.duration / 1000) {
        app.currently_playing.curr_time += 1
    }
}
setInterval(update_progress_bar, 1000)