var object = null,
    commands;

commands = {
    eval: function (command, callback) {
        object = eval(command.expression)
        callback(object)
    },
    attr: function (command, callback) {
        object = object[command.attr]
        callback(object)
    },
    call: function (command, callback) {
        object = object()
        callback(object)
    }
}

function nipCommand(cmd, callback) {
    var func = commands[cmd.command]
    func(cmd, callback)
}

process.stdin.on('data', function (data) {
    var command = JSON.parse('' + data)
    nipCommand(command, write)
})

function write(result) {
    var type = typeof result
    var obj = type === 'undefined' ? null :
        type === 'number' ? result :
        type === 'boolean' ? result :
        type === 'string' ? result :
        result instanceof Array ? result :
        result === null ? null :
        result.toString()

    process.stdout.write(JSON.stringify({
        obj: obj,
        type: type
    }) + '\n')
}

