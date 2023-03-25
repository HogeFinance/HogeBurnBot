const fs = require('fs');
const path = require('path');
const ethers = require('ethers');
const {Telegraf} = require('telegraf');
const {address, abi, dead} = JSON.parse(fs.readFileSync(`./info.hoge`));
const {telegramToken, infuraToken} = JSON.parse(fs.readFileSync(`./burnbot.cfg`));

if (!telegramToken || !infuraToken) return '1';




(async () => {
    console.log('telegram: ',telegramToken != undefined, '\ninfura:', infuraToken != undefined)
    const provider = new ethers.InfuraProvider('homestead', infuraToken);
    const contract = new ethers.Contract(address.eth.hoge, abi.eth.hoge, provider)
    const bot = new Telegraf(telegramToken)

    const slashs = '//////////'
    const burnCmds = ['burn', slashs]
    const infoCmds = ['info', 'cmd', 'commands']
    const allComs = burnCmds.concat(infoCmds)

    bot.command(infoCmds, ctx => {
        getInfo(ctx)
    }) 

    bot.command(burnCmds, ctx => {
        getBurnInfo(ctx)
    })

    bot.launch()
    // Enable graceful stop
    process.once('SIGINT', () => bot.stop('SIGINT'))
    process.once('SIGTERM', () => bot.stop('SIGTERM'))

// functions
//

    function getInfo(ctx){
        console.log(ctx.message.text, ctx.from)
        let comStr = ''
        allComs.forEach(command => {
            comStr = comStr.concat('/', command, '\n')
        });
        bot.telegram.sendMessage(ctx.chat.id, comStr)
    }

    async function getBurnInfo(ctx){
        console.log(ctx.message.text, ctx.from)
        const burn = await contract.balanceOf(dead)
        // simply calc, needs to look at all bridges for lost sent
        const supply = Math.pow(10, 12) - (parseInt(burn) * 10**-9)
        const msg = parseInt(supply).toLocaleString().concat(' HOGE *left*')
        //console.log(parseInt(supply).toLocaleString())
        bot.telegram.sendMessage(ctx.chat.id, msg)
    }

})();
