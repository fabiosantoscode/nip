var commands = {
    eval: function (command, callback) {
        callback(command)
    }
}

function nipCommand(cmd, callback) {
    var func = commands[cmd.command]
    func(cmd, callback)
}

process.stdin
    .on('data', function (data) {
        try {
            command = JSON.parse('' + data)
        } catch (e) {
            process.stderr.write('' + e)
        }

        nipCommand(command, function (res) {
            process.stdout.write(JSON.stringify(res))
        })
    })

