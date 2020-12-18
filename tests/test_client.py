import pytest
from api_trello import TrelloWebHook, TrelloException, TrelloCard, TrelloList, Member


@pytest.mark.parametrize(
    "json_response", [
        # No webhooks set previously
        [],
        # Webhook set correctly
        [{'id': '5fbf92a8a8ceaf0ea2806041', 'description': 'WH for Helpdesk TG Bot', 'idModel': 'bbbbbbbbbb1234567890BBBBBBBBBB00', 'callbackURL': 'http://dc26a2410675.ngrok.io/trello/wh', 'active': True, 'consecutiveFailures': 0, 'firstConsecutiveFailDate': None}],
    ])
@pytest.mark.asyncio
async def test_get_webhooks(client, mock_aioresponse, json_response):
    mock_aioresponse.get(f"https://trello.com/1/tokens/{client.token}/webhooks", payload=json_response)

    response = await client.get_webhooks()
    correct_answer = [TrelloWebHook.parse_obj(wh) for wh in json_response]

    assert type(response) == list
    assert response == correct_answer


@pytest.mark.parametrize(
    "status, content_type, response_type, response_payload", [
        # No HEAD response from webhook
        [400, "application/json", "payload", {'message': f'URL (http://dc26a2410675.ngrok.io/trello/wh) did not return 200 status code, got 405', 'error': 'ERROR'}],
        # Webhook exists
        [400, "text/plain", "body", "A webhook with that callback, model, and token already exists"],
    ])
@pytest.mark.asyncio
async def test_set_webhook_exceptions(client, mock_aioresponse, status, content_type, response_type, response_payload):
    wh_url = 'http://dc26a2410675.ngrok.io/trello/wh'
    mock_aioresponse.post(f"https://trello.com/1/tokens/{client.token}/webhooks", status=status, content_type=content_type, **{response_type: response_payload})

    with pytest.raises(TrelloException) as e:
        response = await client.set_webhook(wh_url, id_model=client.board_id)

    if content_type == "text/plain":
        correct_answer = response_payload
    else:
        correct_answer = response_payload["message"]

    assert type(e.value) == TrelloException
    assert str(e.value) == correct_answer


@pytest.mark.parametrize(
    "status, content_type, response_type, response_payload", [
        # Webhook was set
        [200, "application/json", "payload", {'id': '5fbf82b5b5a77b8b851afad4', 'description': 'WH for Helpdesk TG Bot', 'idModel': 'bbbbbbbbbb1234567890BBBBBBBBBB00', 'callbackURL': 'http://dc26a2410675.ngrok.io/trello/wh', 'active': True, 'consecutiveFailures': 0, 'firstConsecutiveFailDate': None}],
    ])
@pytest.mark.asyncio
async def test_set_webhook(client, mock_aioresponse, status, content_type, response_type, response_payload):
    wh_url = 'http://dc26a2410675.ngrok.io/trello/wh'
    mock_aioresponse.post(f"https://trello.com/1/tokens/{client.token}/webhooks", status=status, content_type=content_type, **{response_type: response_payload})

    response = await client.set_webhook(wh_url, description="WH for Helpdesk TG Bot", id_model=client.board_id)
    correct_answer = TrelloWebHook.parse_obj(response_payload)

    assert type(response) == TrelloWebHook
    assert response == correct_answer


@pytest.mark.parametrize(
    "answer, status, wh_id, content_type, response_type, response_payload", [
        # Webhook does not exist
        [False, 400, "aaaaaaaaaaaaaaaaaaaaaaaa", "text/plain", "body", "invalid value for idWebhook"],
        # Webhook was deleted
        [True, 200, "5fbf82b5b5a77b8b851afad4", "application/json", "payload", {'_value': None}],
        # Attempt to delete webhhok twice
        [False, 404, "5fbf82b5b5a77b8b851afad4", "text/plain", "body", "The requested resource was not found."],
    ])
@pytest.mark.asyncio
async def test_del_webhook(client, mock_aioresponse, answer, status, wh_id, content_type, response_type, response_payload):
    mock_aioresponse.delete(f"https://trello.com/1/tokens/{client.token}/webhooks/{wh_id}", status=status, content_type=content_type, **{response_type: response_payload})

    response = await client.del_webhook(wh_id)

    assert response == answer


@pytest.mark.parametrize(
    "status, id_list, content_type, response_type, response_payload", [
        [400, "", "text/plain", "body", "invalid value for idList"],
    ])
@pytest.mark.asyncio
async def test_create_card_invalid_value(client, mock_aioresponse, status, id_list, content_type, response_type, response_payload):
    mock_aioresponse.post("https://trello.com/1/cards", status=status, content_type=content_type, **{response_type: response_payload})

    with pytest.raises(TrelloException) as e:
        response = await client.create_card(id_list, "New Card", "Card Text")

    assert type(e.value) == TrelloException
    assert str(e.value) == response_payload


@pytest.mark.parametrize(
    "status, id_list, content_type, response_type, response_payload", [
        [200, "5fc10d349569a54078da50fe", "application/json", "payload", {'id': '5fc10d349569a54078da50fe', 'checkItemStates': [], 'closed': False, 'dateLastActivity': '2020-11-27T14:29:08.437Z', 'desc': 'Card Text', 'descData': {'emoji': {}}, 'dueReminder': None, 'idBoard': "MOCK_BOARD_ID", 'idList': "MOCK_LIST_ID", 'idMembersVoted': [], 'idShort': 427, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': '', 'pos': 128, 'shortLink': 'i3D9oTTF', 'isTemplate': False, 'cardRole': None, 'dueComplete': False, 'due': '2020-11-27T19:29:08.072Z', 'labels': [], 'shortUrl': 'https://trello.com/c/i3D9oTTF', 'start': None, 'url': 'https://trello.com/c/i3D9oTTF/427--', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}, 'idMembers': [], 'email': None, 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': True, 'due': '2020-11-27T19:29:08.072Z', 'dueComplete': False, 'start': None}, 'subscribed': False, 'idChecklists': [], 'attachments': [], 'stickers': [], 'limits': {}}],
    ])
@pytest.mark.asyncio
async def test_create_card(client, mock_aioresponse, status, id_list, content_type, response_type, response_payload):
    mock_aioresponse.post("https://trello.com/1/cards", status=status, content_type=content_type, **{response_type: response_payload})

    response = await client.create_card(id_list, "New Card", "Card Text")

    correct_answer = TrelloCard.parse_obj(response_payload)
    assert response == correct_answer


@pytest.mark.parametrize(
    "status, card_id, content_type, response_type, response_payload", [
        [404, "", "text/plain", "body", "Cannot GET /1/cards/"],
        [404, "12312321", "text/plain", "body", "card not found"],
    ])
@pytest.mark.asyncio
async def test_get_card_invalid(client, mock_aioresponse, status, card_id, content_type, response_type, response_payload):
    mock_aioresponse.get(f"https://trello.com/1/cards/{card_id}", status=status, content_type=content_type, **{response_type: response_payload})

    with pytest.raises(TrelloException) as e:
        response = await client.get_card(card_id)

    assert type(e.value) == TrelloException
    assert str(e.value) == response_payload


@pytest.mark.parametrize(
    "status, card_id, content_type, response_type, response_payload", [
        [200, "5fc10d349569a54078da50fe", "application/json", "payload", {'id': '5fc10d349569a54078da50fe', 'address': None, 'checkItemStates': [], 'closed': False, 'coordinates': None, 'creationMethod': None, 'dateLastActivity': '2020-11-27T14:29:08.437Z', 'desc': 'Card Text', 'descData': None, 'dueReminder': None, 'idBoard': '5f43db65a1d25218690c062b', 'idLabels': [], 'idList': '5f43db65a1d25218690c062c', 'idMembersVoted': [], 'idShort': 427, 'idAttachmentCover': None, 'locationName': None, 'manualCoverAttachment': False, 'name': '', 'pos': 128, 'shortLink': 'i3D9oTTF', 'isTemplate': False, 'cardRole': None, 'dueComplete': False, 'due': '2020-11-27T19:29:08.072Z', 'labels': [], 'shortUrl': 'https://trello.com/c/i3D9oTTF', 'start': None, 'url': 'https://trello.com/c/i3D9oTTF/427--', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}, 'idMembers': [], 'limits': {'attachments': {'perCard': {'status': 'ok', 'disableAt': 1000, 'warnAt': 900}}, 'checklists': {'perCard': {'status': 'ok', 'disableAt': 500, 'warnAt': 450}}, 'stickers': {'perCard': {'status': 'ok', 'disableAt': 70, 'warnAt': 63}}}, 'email': None, 'idChecklists': [], 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': True, 'due': '2020-11-27T19:29:08.072Z', 'dueComplete': False, 'start': None}, 'subscribed': False, 'checklists': [], 'customFieldItems': []}],
    ])
@pytest.mark.asyncio
async def test_get_card(client, mock_aioresponse, status, card_id, content_type, response_type, response_payload):
    mock_aioresponse.get(f"https://trello.com/1/cards/{card_id}", status=status, content_type=content_type, **{response_type: response_payload})

    response = await client.get_card(card_id)

    correct_answer = TrelloCard.parse_obj(response_payload)
    assert response == correct_answer


@pytest.mark.parametrize(
    "status, card_id, content_type, response_type, response_payload", [
        [404, "", "text/plain", "body", "Cannot PUT /1/cards/"],
        [400, "12312321", "text/plain", "body", "invalid id"],
    ])
@pytest.mark.asyncio
async def test_update_card_invalid(client, mock_aioresponse, status, card_id, content_type, response_type, response_payload):
    mock_aioresponse.put(f"https://trello.com/1/cards/{card_id}", status=status, content_type=content_type, **{response_type: response_payload})

    with pytest.raises(TrelloException) as e:
        response = await client.update_card(card_id, name="New name card")

    assert type(e.value) == TrelloException
    assert str(e.value) == response_payload


@pytest.mark.parametrize(
    "status, card_id, content_type, response_type, response_payload", [
        [200, "5fc10d349569a54078da50fe", "application/json", "payload",  {'id': '5fc10d349569a54078da50fe', 'checkItemStates': [], 'closed': False, 'dateLastActivity': '2020-11-27T14:57:07.141Z', 'desc': 'Card Text', 'descData': None, 'dueReminder': None, 'idBoard': '5f43db65a1d25218690c062b', 'idList': '5f43db65a1d25218690c062c', 'idMembersVoted': [], 'idShort': 427, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': 'New name card', 'pos': 128, 'shortLink': 'i3D9oTTF', 'isTemplate': False, 'cardRole': None, 'dueComplete': False, 'due': '2020-11-27T19:29:08.072Z', 'labels': [], 'shortUrl': 'https://trello.com/c/i3D9oTTF', 'start': None, 'url': 'https://trello.com/c/i3D9oTTF/427-new-name-card', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}, 'idMembers': [], 'email': None, 'idChecklists': [], 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': True, 'due': '2020-11-27T19:29:08.072Z', 'dueComplete': False, 'start': None}, 'subscribed': False}],
    ])
@pytest.mark.asyncio
async def test_update_card(client, mock_aioresponse, status, card_id, content_type, response_type, response_payload):
    mock_aioresponse.put(f"https://trello.com/1/cards/{card_id}", status=status, content_type=content_type, **{response_type: response_payload})

    response = await client.update_card(card_id, name="New name card")

    correct_answer = TrelloCard.parse_obj(response_payload)
    assert response == correct_answer


@pytest.mark.asyncio
async def test_get_lists(client, mock_aioresponse):
    JSON_RESPONSE = [{'id': '5f43db65a1d25218690c062c', 'name': 'Новая задача', 'closed': False, 'pos': 16384, 'softLimit': None, 'idBoard': client.board_id, 'subscribed': False},
                     {'id': '5f43db65a1d25218690c062d', 'name': 'В работе', 'closed': False, 'pos': 32768, 'softLimit': None, 'idBoard': client.board_id, 'subscribed': False},
                     {'id': '5f43ebe557a419018bb34b4b', 'name': 'Требуется помощь IT', 'closed': False, 'pos': 40960, 'softLimit': None, 'idBoard': client.board_id, 'subscribed': False},
                     {'id': '5f43db65a1d25218690c062e', 'name': 'Завершена', 'closed': False, 'pos': 106496, 'softLimit': None, 'idBoard': client.board_id, 'subscribed': False}]
    mock_aioresponse.get(f"https://trello.com/1/boards/{client.board_id}/lists", payload=JSON_RESPONSE)

    response = await client.get_lists()
    assert type(response) == list
    assert response == [TrelloList.parse_obj(lst) for lst in JSON_RESPONSE]


@pytest.mark.parametrize(
    "status, card_id, memder_id, content_type, response_type, response_payload", [
        [400, "5fc10d349569a54078da50fe", "5a214fe083df8aa8c81899e8", "text/plain", "body", "member is already on the card"],
        [400, "5fc10d349569a54078da50fe", "", "text/plain", "body", "invalid value for value"],
        [400, "5fc10d349569a54078da50fe", "123123123", "text/plain", "body", "invalid value for value"],
        [404, "", "5a214fe083df8aa8c81899e8", "text/plain", "body", "Cannot POST /1/cards//idMembers"],
    ])
@pytest.mark.asyncio
async def test_add_member_invalid(client, mock_aioresponse, status, card_id, memder_id, content_type, response_type, response_payload):
    mock_aioresponse.post(f"https://trello.com/1/cards/{card_id}/idMembers", status=status, content_type=content_type, **{response_type: response_payload})
    with pytest.raises(TrelloException) as e:
        response = await client.add_member(card_id, memder_id)
    assert type(e.value) == TrelloException
    assert str(e.value) == response_payload


@pytest.mark.parametrize(
    "status, card_id, memder_id, content_type, response_type, response_payload", [
        [200, "5fc10d349569a54078da50fe", "5a214fe083df8aa8c81899e8", "application/json", "payload",  [{'id': '5a214fe083df8aa8c81899e8', 'username': 'herr_horror', 'activityBlocked': False, 'avatarHash': '907ce73a28929a01448eca6e46abdc1b', 'avatarUrl': 'https://trello-members.s3.amazonaws.com/5a214fe083df8aa8c81899e8/907ce73a28929a01448eca6e46abdc1b', 'fullName': 'herr_horror', 'idMemberReferrer': None, 'initials': 'H', 'nonPublic': {}, 'nonPublicAvailable': True}]],
    ])
@pytest.mark.asyncio
async def test_add_member(client, mock_aioresponse, status, card_id, memder_id, content_type, response_type, response_payload):
    mock_aioresponse.post(f"https://trello.com/1/cards/{card_id}/idMembers", status=status, content_type=content_type, **{response_type: response_payload})
    response = await client.add_member(card_id, memder_id)
    correct_answer = [Member.parse_obj(m) for m in response_payload]
    assert type(response) == list
    assert response == correct_answer