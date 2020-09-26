import time

def server_stuff(bot):
    while True:
        try:
            if bot.running:
                resp = bot.get_resp()

                # On connection success
                if resp == 1:
                    for channel in bot.channels:
                        bot.join_channel(channel)

                # Suppress server messages
                if bot.suppress:
                    for s in bot.suppress:
                        if s in resp:
                            resp = None

                if resp:
                    for s in bot.script_msg_switches:
                        bot.script_msg_switches[s] = True

                    bot.new_msg = True
                    bot.message_queue.append(resp)
                    print(bot.message_queue[-1])
        except:
            pass

        time.sleep(.5)
