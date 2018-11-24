from django.db.models import Q

from .models import Transfer


def is_sender(user, transfer):
    return transfer.sender == user


def generate_suitable_transfers(user):
    transfers_list = []
    transfers_staged = []

    suitable_transfers = Transfer.objects.filter(
        Q(sender=user) | Q(receiver=user)
    )

    for transfer in suitable_transfers:
        if not transfer.is_staged:
            transfer_dict = {
                'id': transfer.id,
                'receiver': transfer.receiver.username,
                'sender': transfer.sender.username,
                'amount': transfer.amount,
                'is_sender': transfer.sender == user,
                'data': transfer.date
            }
            transfers_list.append(
                transfer_dict
            )
        else:
            transfer_dict = {
                'id': transfer.id,
                'receiver': transfer.receiver.username,
                'sender': transfer.sender.username,
                'amount': transfer.amount,
                'is_sender': transfer.sender == user,
                'data': transfer.date
            }
            transfers_staged.append(
                transfer_dict
            )

        transfers_list.sort(key=lambda item:item['data'], reverse=True)
        transfers_staged.sort(key=lambda item:item['data'], reverse=True)

    return transfers_list, transfers_staged
