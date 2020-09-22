import json
import socket

'''
commands = {
    'PRIVMSG': 
}
'''

def console_stuff(bot, conn):
    try:
        conn.send(bytes(get_bot_state(bot), "UTF-8"))
    except:
        pass

    while True:        
        try:
            data = conn.recv(2048).decode("UTF-8")
        except:
            break

        if data:
            try:
                command = json.loads(data)            
                if command['query type'] == 'server_action':
                    if command['action'] == "PRIVMSG":
                        for e in command['entity']:
                            bot.send_msg(e, command['message'])      
                    
                    if command['action'] == 'mode':
                            bot.send_msg(message=command['message'])

                    if command['action'] == '/join':
                        for chan in command['target']:
                            bot.join_channel(chan)
                            time.sleep(0.5)

                    if command['action'] == '/part':
                        for chan in command['target']:
                            bot.part_channel(chan)
                            time.sleep(0.5)

                    if command['action'] == '/users':
                        bot.send_msg(message=command['message'])
                
                if command['query type'] == 'bot_action':
                    if command['action'] == 'disconnect':
                        print("Disconnecting from server.")
                        time.sleep(2)
                        irc.send(bytes("QUIT" + "\n", "UTF-8"))
                        bot.irc.close()
                        bot.running = False
                    
                    if command['action'] == "connect":
                        try:
                            bot.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            for server in config.servers:
                                bot.connect(server, config.servers[server])
                        except Exception as e:
                            print(e)
                    
                    if command['action'] == 'load script':
                        script = command['target']


                        if script in bot.current_scripts:
                            response = "Module already loaded"

                        else:
                            try:
                                bot.script_msg_switches[script] = False

                                module = importlib.import_module(script)
                                instance = importlib.reload(module).get_instance(bot)
                                bot.current_scripts[script] = instance
                                sthread = threading.Thread(target=instance.main_thread)
                                threads[script] = sthread
                                sthread.start()
                                print("%s loaded" % (script))
                            except:
                                print("Could not load module")

                    if command['action'] == 'reload script':
                        script = command['target']

                        try:
                            bot.current_scripts[script].running = False
                            #threads[script].join()

                            module = importlib.import_module(script)
                            new_instance = importlib.reload(module).get_instance(bot)
                            bot.current_scripts[script] = new_instance
                            sthread = threading.Thread(target=new_instance.main_thread)
                            threads[script] = sthread
                            sthread.start()
                            print("%s reloaded" % (script))

                        except Exception as e:
                            print(e)
                        
                if command['query type'] == 'script_action':
                    script = command['entity']

                    if command['action'] == 'list_vars':
                        script_vars = json.dumps(bot.current_scripts[script].get_env())

                        try:
                            conn.send(bytes(script_vars, "UTF-8"))
                        except:
                            pass

                    if command['action'] == 'set_var':
                        script_var = command['target']
                        var_value = command['var_value']
                        print(script_var, var_value)

                        if var_value == 'False' or var_value == 'True':
                            try:
                                setattr(bot.current_scripts[script], script_var, json.loads(var_value.lower()))
                                msg = "%s has been changed to %s" % (script_var, var_value)
                                response = get_bot_state(bot, msg)
                                conn.send(bytes(response, "UTF-8"))

                            except Exception as e:
                                print(e)

            except Exception as e:
                pass
        
        data = None
        bot.script_state_update = False
        time.sleep(.2)