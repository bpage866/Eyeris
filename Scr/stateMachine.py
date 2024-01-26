
class StateMachine():
    def __init__(self, states):
        self.states = states
        self.current = list(states.values())[0]
    def addState(self, name, state):
        self.states[name] = state

    def change(self, state, change):
        self.current = self.states[state]
        self.current.changes(change)
    def update(self,dt, keys, screen):
        self.current.update(dt, keys, screen)
    def render(self, screen):
        self.current.render(screen)

class EnitiyStateMachine(StateMachine):
    def update(self,dt, keys, extras):
        self.current.update(dt,keys, extras)