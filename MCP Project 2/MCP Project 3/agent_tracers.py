import string

import secrets

from equity_database import update_equity_database_log

from agents import TracingProcessor, Span, Trace

ALPHANUMERIC = string.ascii_lowercase + string.digits

def generate_agent_trace_id(agent_tag: str) -> str:

    agent_tag += '0'

    pad_length = 32 - len(agent_tag)

    random_suffix = ''.join(secrets.choice(ALPHANUMERIC) for _ in range(pad_length))

    return f'{agent_tag}{random_suffix}'

class LogTracer(TracingProcessor):

    def get_agent_trace_name(self, trace_or_span: Trace | Span ) -> str | None:

        agent_trace_id = trace_or_span.trace_id

        agent_trace_name = agent_trace_id.split('_')[1]

        if '0' in agent_trace_name:

            return agent_trace_name.split('0')[0]
        else:

            return None  

    def on_agent_trace_initialization(self, agent_trace) -> None:

        agent_trace_name = self.get_agent_trace_name(agent_trace)

        if agent_trace_name:

            update_equity_database_log(log_name=agent_trace, log_type= 'agent trace', log_message = f'Started {agent_trace}')

    
    def on_agent_trace_termination(self, agent_trace) -> None:

        agent_trace_name = self.get_agent_trace_name(agent_trace)

        if agent_trace_name:

            update_equity_database_log(log_name = agent_trace, log_type = 'agent trace', log_message= f'Ended {agent_trace}')


    def on_agent_span_initialization(self, agent_span) -> None:

        agent_span_name = self.get_agent_trace_name(agent_span)

        agent_span_type = agent_span.span_data.type if agent_span.span_data else 'agent span'

        if agent_span_name:

            message = 'Starting span'

            if agent_span.span_data:

                if agent_span.span_data.type:

                    message += f'{agent_span.span_data.type}'

                if hasattr(agent_span.span_data, 'agent span name') and agent_span.span_data.agent_span_name:

                    message += f'{agent_span.span_data.agent_span_name}'

                if hasattr(agent_span.span_data, 'server') and agent_span.span_data.server:

                    message += f'{agent_span.span_data.server}'

                if agent_span.error:

                    message += f'{agent_span.error}'
                
                update_equity_database_log(log_name = agent_span_name, log_type = agent_span_type, log_message = message)
    
    def on_agent_span_termination(self, agent_span) -> None:

        agent_span_name =  self.get_agent_trace_name(agent_span) 

        agent_span_type = agent_span.span_data.type if agent_span.span_data else 'agent span'

        message = 'Span terminated'

        if agent_span.span_data:

            if agent_span.span_data.type:

                message += f'{agent_span.span_data.type}'

            if hasattr(agent_span.span_data, 'agent_span_name') and agent_span.span_data.agent_span_name:

                message += f'{agent_span.span_data.agent_span_name}'

            if hasattr(agent_span.span_data, 'server') and agent_span.span_data.server:

                message += f'{agent_span.span_data.server}'

            if agent_span.error:

                message += f'{agent_span.error}'

            update_equity_database_log(log_name=agent_span_name, log_type= agent_span_type, log_message= message)

    
    def force_flush(self) -> None:

        pass
    
    def shutdown(self) -> None:
        
        pass



    