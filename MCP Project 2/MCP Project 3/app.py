from agent_user_interface import build_gradio_user_interface

if __name__ == '__main__':

 agent_trading_platform = build_gradio_user_interface()

 agent_trading_platform.launch(inbrowser=True, debug = True)