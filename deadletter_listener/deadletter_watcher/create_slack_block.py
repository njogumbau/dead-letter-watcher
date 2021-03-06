from typing import Dict, List, Union
from deadletter_watcher.slack_blocks.deadletter import create_deadletter_slack_block
from deadletter_watcher.slack_blocks.actions import create_actions_slack_block
from deadletter_watcher.slack_blocks.welcome import create_welcome_slack_block
from deadletter_watcher.slack_blocks.options import create_options_slack_block


def create_slack_block(cluster: str, service: str, count: Union[int, str],
                       deadletters: List[Dict]) -> List[Dict]:
    """Create a Slack Block from deadletter information
    Args:
        cluster: affected cluster
        service: affected service bus
        count: number of deadletters in service bus
        deadletters: List of Dicts containg deadletter information
        Dict Keys Required
        'message_id':str, 'tenant_name':str, 'sender':str, 'recipient':str
    Returns:
        List of Slack Blocks ready to be transmitted to Slack.
    """
    block = []

    block.append(create_welcome_slack_block(cluster, service, count))

    block.append({"type": "divider"})

    for deadletter in deadletters:
        deadletter_slack_block = create_deadletter_slack_block(
            trx_id=deadletter['message_id'],
            tenant=deadletter['tenant_name'],
            sender=deadletter['sender'],
            receiver=deadletter['recipient'],
            timestamp=deadletter['timestamp']
        )

        block.append(deadletter_slack_block)

        actions={
            "type": "actions",
            "elements": create_options_slack_block(deadletter['message_id'], ["Replay", "Reconstruct"])
        }
        block.append(actions)

        block.append({"type": "divider"})

    #block.append(create_actions_slack_block())

    return block
