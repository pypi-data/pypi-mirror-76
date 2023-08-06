<a name="aea.aea"></a>
# aea.aea

This module contains the implementation of an autonomous economic agent (AEA).

<a name="aea.aea.AEA"></a>
## AEA Objects

```python
class AEA(Agent,  WithLogger)
```

This class implements an autonomous economic agent.

<a name="aea.aea.AEA.__init__"></a>
#### `__`init`__`

```python
 | __init__(identity: Identity, wallet: Wallet, resources: Resources, loop: Optional[AbstractEventLoop] = None, timeout: float = 0.05, execution_timeout: float = 0, max_reactions: int = 20, decision_maker_handler_class: Type[
 |             DecisionMakerHandler
 |         ] = DefaultDecisionMakerHandler, skill_exception_policy: ExceptionPolicyEnum = ExceptionPolicyEnum.propagate, loop_mode: Optional[str] = None, runtime_mode: Optional[str] = None, default_connection: Optional[PublicId] = None, default_routing: Optional[Dict[PublicId, PublicId]] = None, connection_ids: Optional[Collection[PublicId]] = None, search_service_address: str = "fetchai/soef:*", **kwargs, ,) -> None
```

Instantiate the agent.

**Arguments**:

- `identity`: the identity of the agent
- `wallet`: the wallet of the agent.
- `resources`: the resources (protocols and skills) of the agent.
- `loop`: the event loop to run the connections.
- `timeout`: the time in (fractions of) seconds to time out an agent between act and react
- `exeution_timeout`: amount of time to limit single act/handle to execute.
- `max_reactions`: the processing rate of envelopes per tick (i.e. single loop).
- `decision_maker_handler_class`: the class implementing the decision maker handler to be used.
- `skill_exception_policy`: the skill exception policy enum
- `loop_mode`: loop_mode to choose agent run loop.
- `runtime_mode`: runtime mode (async, threaded) to run AEA in.
- `default_connection`: public id to the default connection
- `default_routing`: dictionary for default routing.
- `connection_ids`: active connection ids. Default: consider all the ones in the resources.
- `search_service_address`: the address of the search service used.
- `kwargs`: keyword arguments to be attached in the agent context namespace.

**Returns**:

None

<a name="aea.aea.AEA.decision_maker"></a>
#### decision`_`maker

```python
 | @property
 | decision_maker() -> DecisionMaker
```

Get decision maker.

<a name="aea.aea.AEA.context"></a>
#### context

```python
 | @property
 | context() -> AgentContext
```

Get (agent) context.

<a name="aea.aea.AEA.resources"></a>
#### resources

```python
 | @property
 | resources() -> Resources
```

Get resources.

<a name="aea.aea.AEA.resources"></a>
#### resources

```python
 | @resources.setter
 | resources(resources: "Resources") -> None
```

Set resources.

<a name="aea.aea.AEA.task_manager"></a>
#### task`_`manager

```python
 | @property
 | task_manager() -> TaskManager
```

Get the task manager.

<a name="aea.aea.AEA.setup_multiplexer"></a>
#### setup`_`multiplexer

```python
 | setup_multiplexer() -> None
```

Set up the multiplexer.

<a name="aea.aea.AEA.filter"></a>
#### filter

```python
 | @property
 | filter() -> Filter
```

Get the filter.

<a name="aea.aea.AEA.active_behaviours"></a>
#### active`_`behaviours

```python
 | @property
 | active_behaviours() -> List[Behaviour]
```

Get all active behaviours to use in act.

<a name="aea.aea.AEA.setup"></a>
#### setup

```python
 | setup() -> None
```

Set up the agent.

Performs the following:

- loads the resources (unless in programmatic mode)
- starts the task manager
- starts the decision maker
- calls setup() on the resources

**Returns**:

None

<a name="aea.aea.AEA.act"></a>
#### act

```python
 | act() -> None
```

Perform actions.

Calls act() of each active behaviour.

**Returns**:

None

<a name="aea.aea.AEA.react"></a>
#### react

```python
 | react() -> None
```

React to incoming envelopes.

Gets up to max_reactions number of envelopes from the inbox and
handles each envelope, which entailes:

- fetching the protocol referenced by the envelope, and
- returning an envelope to sender if the protocol is unsupported, using the error handler, or
- returning an envelope to sender if there is a decoding error, using the error handler, or
- returning an envelope to sender if no active handler is available for the specified protocol, using the error handler, or
- handling the message recovered from the envelope with all active handlers for the specified protocol.

**Returns**:

None

<a name="aea.aea.AEA.update"></a>
#### update

```python
 | update() -> None
```

Update the current state of the agent.

Handles the internal messages from the skills to the decision maker.

:return None

<a name="aea.aea.AEA.teardown"></a>
#### teardown

```python
 | teardown() -> None
```

Tear down the agent.

Performs the following:

- stops the decision maker
- stops the task manager
- tears down the resources.

**Returns**:

None

