from agent import Agent

if __name__ == '__main__':
    agent = Agent()
    try:
        agent.start()
    except KeyboardInterrupt:
        agent.shutdown()
