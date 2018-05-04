from rest_framework import viewsets
from rest_framework.response import Response
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from app.utils import dictfetchall
from delphi.constants import STAGE_CHOICES
from delphi.models import Token
from delphi.queries import LEADERBOARD_QUERY
from delphi.serializers import TokenSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend

# class BountyStats(APIView):
#     def get(self, request, address=''):
#         bounty_stats = {}
#         user_bounties = Bounty.objects.filter(issuer=address.lower())
#         for stage in STAGE_CHOICES:
#             bounty_stats[stage[1]] = user_bounties.filter(
#                 bountyStage=stage[0]).count()
#         bounties_count = user_bounties.count()
#         bounties_accepted_count = user_bounties.filter(
#             fulfillments__accepted=True).count()
#         bounties_acceptance_rate = bounties_accepted_count / \
#             bounties_count if bounties_accepted_count > 0 else 0
#         user_submissions = Fulfillment.objects.filter(fulfiller=address)
#         submissions_count = user_submissions.count()
#         submissions_accepted_count = user_submissions.filter(
#             accepted=True).count()
#         submissions_acceptance_rate = submissions_accepted_count / \
#             submissions_count if submissions_count > 0 else 0
#         profile_stats = {
#             'bounties': bounties_count,
#             'bounties_accepted': bounties_accepted_count,
#             'bounties_acceptance_rate': bounties_acceptance_rate,
#             'submissions': submissions_count,
#             'submissions_accepted_count': submissions_accepted_count,
#             'submissions_acceptance_rate': submissions_acceptance_rate,
#         }
#         return JsonResponse({**bounty_stats, **profile_stats})


class Tokens(APIView):
    def get(self, request):
        token_qs = {}
        result = []
        token_to_append = {}
        token_count = {}
        token_count = Bounty.objects.values('tokenSymbol','tokenContract',
        'tokenDecimals').annotate(count=Count('tokenSymbol')).order_by('-count')
        for bounty in token_count:
            token_to_append = {}
            token_to_append.update(bounty)
            token_qs = Token.objects.filter(symbol=bounty['tokenSymbol'])
            if token_qs.count() > 0:
                serializer = TokenSerializer(token_qs, many=True)
                token_to_append['token'] = serializer.data
            else:
                token_to_append['token'] = []
            result.append(token_to_append)
        return JsonResponse(result, safe=False)
