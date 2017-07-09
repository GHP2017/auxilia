
socket = io.connect('http://' + document.domain + ':' + location.port);

$.ajaxSetup({
  xhrFields: {
    withCredentials: true
  }
});

socket.on('connect', function() {
    socket.emit('client_connected', {data: 'I\'m connected!'});
});

socket.on('queue_changed', function(data) {
    console.log('the queue is updating')
    for (i = 0; i < data.length; i ++) {
        song = data[i]
        matched = false
        for (j = 0; j < app.queue.length; j ++) {
            if (song.track_id == app.queue[j].track_id) {
                matched = true
                song['was_upvoted'] = app.queue[j]['was_upvoted'];
                song['was_downvoted'] = app.queue[j]['was_downvoted'];
                break;
            }
        }
        if (!matched) {
            song['was_upvoted'] = false;
            song['was_downvoted'] = false;
        }
        
    }
    app.queue = data;
});

socket.on('suggestions_changed', function(data) {
    console.log('new suggestions inbound');
    app.suggestions = data;
});

socket.on('currently_playing_changed', function (data) {
    console.log('next song')
    setTimeout(update_currently_playing, 5000, data, 0)
})

socket.on('mid_currently_playing', function (data) {
    curr_time = Date.now() - data['time_played'] * 1000
    curr_time /= 1000
    update_currently_playing(data, curr_time)
})

socket.on('synchronize_thumbs', function (data) {
    console.log(data)
})

update_currently_playing = function (data, curr_time ) {
    app.curr_album_name = data['album_name']
    app.curr_album_uri = data['album_uri']
    app.curr_name = data['name']
    app.curr_artist = data['artist']
    app.curr_duration = data['duration']
    app.curr_duration_display = ''
    app.curr_time = curr_time
    app.curr_time_display = ''
}

socket.on('paused', function(data) {
    app.paused = true
});

socket.on('resume', function(data) {
    app.paused = false
});

submit_song_url = '/add_song?song=spotify:track:'
thumbs_url = '/thumbs_change'

Vue.use(VueTouch, {name: 'v-touch'})

app = new Vue({
    el: '#app',
    data: {
        queue: [],
        search: '',
        suggestions: [],
        paused: false,
        show_error: false,
        error_message: '',
        curr_album_name: '',
        curr_album_uri: '',
        curr_name: '',
        curr_artist: '',
        curr_duration: 0,
        curr_duration_display: '',
        curr_time: 0,
        curr_time_display: ''
    },
    watch: {
        search: _.debounce (function () {
            if (this.search != '') {
                socket.emit('searchbar_changed', {query: this.search})
            }
            else {
                this.suggestions = []
            }
        }, 750),
        curr_time: function () {
            app.curr_time_display = this.format_duration(this.curr_time * 1000)
        },
        curr_duration: function () {
            app.curr_duration_display = this.format_duration(this.curr_duration)
        }
    },
    methods: {
        submit_song: function (track_id) {
            console.log('submitting...')
            $.ajax(submit_song_url + track_id).done(function (data) {
                data = JSON.parse(data)
                if (data.error != undefined) {
                    console.log(data.error)
                    app.error_message = data.error
                    app.show_error = true
                    setTimeout(reset_error, 10000)
                }
                app.search = ''
            }).fail(function (data) {
                console.log('failure')
            })
        },
        upvote: function (index) {
            song = this.queue[index]
            console.log('upvote')
            if (song['was_upvoted']) {
                song['was_upvoted'] = false
                $.post(thumbs_url, {track_id: song.track_id, change: 'up', decrement: true})
            }
            else {
                song['was_upvoted'] = true
                $.post(thumbs_url, {track_id: song.track_id, change: 'up', decrement: false})
                if (song['was_downvoted']) {
                    song['was_downvoted'] = false
                    $.post(thumbs_url, {track_id: song.track_id, change: 'down', decrement: true})
                }
            }
        },
        downvote: function (index) {
            song = this.queue[index]
            console.log('downvote')
            if (song['was_downvoted']) {
                song['was_downvoted'] = false
                $.post(thumbs_url, {track_id: song.track_id, change: 'down', decrement: true})
            }
            else {
                song['was_downvoted'] = true
                $.post(thumbs_url, {track_id: song.track_id, change: 'down', decrement: false})
                if (song['was_upvoted']) {
                    song['was_upvoted'] = false
                    $.post(thumbs_url, {track_id: song.track_id, change: 'up', decrement: true})
                }
            }
        },
        format_duration: function(ms) {
            seconds = ms / 1000
            minutes = Math.floor(seconds / 60)
            seconds = Math.round(seconds % 60)
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            return minutes + ':' + seconds
        }
    }
});

// init
$.ajax('/connect').done(function (data) {
    setTimeout(init_final_setup, 2000, data)
})

init_final_setup = function (data) {
    data = JSON.parse(data)
    console.log(data)
    try { 
        keys = Object.keys(data)
        for (i = 0; i < keys.length; i ++) {
            key = keys[i]
            console.log(app.queue.length)
            for (j = 0; j < app.queue.length; j ++) {
                console.log('iterating..')
                song = app.queue[j]
                console.log(song)
                if (song.track_id == key) {
                    console.log('matching song')
                    song.was_upvoted = data[key].was_upvoted
                    song.was_downvoted = data[key].was_downvoted
                }
            }
        }
    } catch(err) {
        // do nothing, data must be empty
        console.log(err)
    }
}
update_progress_bar = function () {
    if (app.curr_time < app.curr_duration / 1000 && !app.paused) {
        app.curr_time += 1
    }
}

reset_error = function() {
    app.show_error = false
    app.error_message = ''
}
setInterval(update_progress_bar, 1000)