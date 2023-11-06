# SWML Python SDK

The SWML Python SDK allows you to generate SWML (SignalWire Markup Language) in Python. SWML is a markup language used to control phone call behavior. This SDK provides classes for each SWML instruction and a convenient way to build sections and responses.

## Installation

You can install the SWML Python SDK via pip:

```bash
pip install swml-python
```

## Documentation
For more details on SWML, please visit the official 
[SignalWire SWML documentation.](https://developer.signalwire.com/sdks/reference/swml/introduction)

## Getting Started
To generate SWML with the SDK, you'll first create an instance of SWMLResponse. This object represents an entire SWML response.

Within a response, you can create one or more **"sections"**. Each section is a collection of instructions that are 
executed in when called. You create a section using the `add_section` method and give it a name:

```python
response = SignalWireML()
main_section = response.add_section('main')
other_section = response.add_section('other')
```

Additionally, you can create a section by creating an instance of the Section class and adding it to the `SignalWireML` object:

```python
main_section = Section('main')
response.add_section(main_section)
```

## Adding Instructions

Once you have a section, you can add instructions to it. Each instruction corresponds to a SWML verb, such as 
**Answer**, **Hangup**, or **Play**. You can add an instruction using the corresponding method on the section object:

```python
response = SignalWireML()
main_section = response.add_section('main')
main_section.answer(max_duration=30)
main_section.play(url="https://example_1.com")
main_section.hangup()
```

In this example, we've added three instructions to the main section: an Answer instruction, a Play instruction, 
and a Hangup instruction.


You can also add instructions by creating instances of the instruction classes and adding them to the section using the
**add_instruction** method. This is useful when you need to create complex instructions that have many parameters or if 
you want to use the same instance declaration in multiple parts of your code:

```python
send_sms_instance = SendSMS(to_number="+1XXXXXXXXXX", from_="+1XXXXXXXXXX", body="Message Body", media=["url1", "url2"],
                            region="us", tags=["Custom", "data"])
main_section.add_instruction(send_sms_instance)
```

In addition, you can add raw SWML JSON to a section using the **add_instruction** method. This can be useful when you have
existing SWML JSON that you want to include in a section:

```python
raw_swml_json = '{"send_sms": {"to_number": "+1XXXXXXXXXX", "from": "+1XXXXXXXXXX", "body": "Message Body", "media": ["url1", "url2"], "region": "us", "tags": ["Custom", "data"]}}'
main_section.add_instruction(raw_swml_json)
```

**Warning:**

When adding raw SWML JSON, you must ensure that the JSON is valid. The SDK does not validate the JSON is valid SWML before
adding it to the section. This approach is flexible and allows the SDK to support new SWML instructions as they are
released, but it also allows you to add invalid SWML to a section. It is advised that you use the SDK methods to add
instructions whenever possible.


## Generating SWML
Once you've added all the desired sections and instructions, you can generate the SWML from the response using the 
**generate_swml** method. This method has the option to output the SWML response in **JSON** or **YAML** format 
(defaults to JSON) utilizing the **format** parameter:

```python
swml = response.generate_swml() # uses JSON as default
print(swml)

swml = response.generate_swml('yaml') # both 'json' and 'yaml' are valid values.
print(swml)
```

You can also convert the response directly to a string to get a json response:

```python
response = SignalWireML()
main_section = response.add_section('main')
main_section.answer()
main_section.hangup()

print(str(response))
```

This will output a string of SWML that represents the response.

## Full Example

Here's a full example that puts everything together:

```python
from swml import *

response = SignalWireML()

main_section = response.add_section("main")
main_section.answer()

main_section.record(stereo=True, format_='mp3')
# Add the prompt instruction
prompt_instruction = Prompt(
    play="say:Please say an input",
    say_language="en-US",
    max_digits=1,
    speech_hints=["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
)
main_section.add_instruction(prompt_instruction)

# Add the switch instruction
switch_instruction = Switch(
    variable="prompt_value",
    case={
        "1": [Transfer(dest="sales")],
        "one": [Transfer(dest="sales")]
    },
    default=[
        Play(url="say:That was a bad input, please try again!"),
        Transfer(dest="main")
    ]
)
main_section.add_instruction(switch_instruction)
sales_section = response.add_section('sales')
sales_section.play(url='say:Welcome to Sales')
sales_section.prompt(
    play='say:Pick a number between 1 and 3',
    say_language="en-US",
    max_digits=1,
    speech_hints=["one", "two", "three"]
)

sales_case = {
    '1': [Play(url="say:Case 1 was chosen"), Hangup()],
    'one': [Play(url="say:Case one was chosen"), Hangup()],
    '2': [Play(url='say:Case 2 was chosen'), Hangup()],
    'two': [Play(url='say:Case two was chosen'), Hangup()],
    '3': [Play(url='say:Case 3 was chosen'), Hangup()],
    'three': [Play(url='say:Case three was chosen'), Hangup()]

}
sales_section.switch(variable='prompt_value', case=sales_case, default=[Transfer(dest='sales')])

swml = response.generate_swml(data_format='yaml')
print(swml)
```

Which will give the following yaml output:

```yaml
sections:
  main:
  - answer
  - record:
      stereo: true
      format: mp3
  - prompt:
      play: say:Please say an input
      say_language: en-US
      max_digits: 1
      speech_hints:
      - one
      - two
      - three
      - four
      - five
      - six
      - seven
      - eight
      - nine
  - switch:
      variable: prompt_value
      case:
        '1':
        - transfer:
            dest: sales
        one:
        - transfer:
            dest: sales
      default:
      - play:
          url: say:That was a bad input, please try again!
      - transfer:
          dest: main
  sales:
  - play:
      url: say:Welcome to Sales
  - prompt:
      play: say:Pick a number between 1 and 3
      say_language: en-US
      max_digits: 1
      speech_hints:
      - one
      - two
      - three
  - switch:
      variable: prompt_value
      case:
        '1':
        - play:
            url: say:Case 1 was chosen
        - hangup
        one:
        - play:
            url: say:Case one was chosen
        - hangup
        '2':
        - play:
            url: say:Case 2 was chosen
        - hangup
        two:
        - play:
            url: say:Case two was chosen
        - hangup
        '3':
        - play:
            url: say:Case 3 was chosen
        - hangup
        three:
        - play:
            url: say:Case three was chosen
        - hangup
      default:
      - transfer:
          dest: sales
```