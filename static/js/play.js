var log = function(){
    console.log(arguments)
}

// 当媒介已就绪可以开始播放时运行的脚本。
function myplay(){
    log('play')
}

// 当媒介被用户或程序暂停时运行的脚本。
function mypause(){

}

// 当媒介已到达结尾时运行的脚本（可发送类似“感谢观看”之类的消息）。
function myended(){

}


$(document).ready(function(){
    var log = function(){
        console.log(arguments)
    }

    log('begin')

    // 获得 playlist
    var playlistArry = new Array()
    for(var i=0; i < $('.item-playlist').length; i++){
        playlistArry[i] = new Array()
        playlistArry[i][0] = $(`.item-title:eq(${i})`).text()
        playlistArry[i][1] = $(`.item-url:eq(${i})`).text()
        playlistArry[i][2] = $(`.item-img-url:eq(${i})`).text()
    }
    // log(playlistArry)
    var media = $('#media')

    // var media = $('#media')[0];  
    // 当媒介被用户或程序暂停时运行的脚本。
    document.getElementById('media').addEventListener('pause', function(){
            log('pause')
    })
    var audioTimer = null; 

    // 播放结束时调用
    document.getElementById('media').addEventListener('ended', function(){
            log('ended')

            var len = $('.item-playlist').length
            var item = parseInt(Math.random() * len)
            var title = playlistArry[item][0]
            var url = playlistArry[item][1]
            var img_url = playlistArry[item][2]

            $('.title-playbar').text(title)
            $('.img-playbar').attr('src', img_url)
            $('#media').attr('src', url)
    })

    
})