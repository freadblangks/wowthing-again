﻿using System.Net.Http;
using Wowthing.Backend.Models.API.Character;
using Wowthing.Lib.Models.Player;
using Wowthing.Lib.Models.Query;

namespace Wowthing.Backend.Jobs.Character
{
    public class CharacterSoulbindsJob : JobBase
    {
        private const string ApiPath = "profile/wow/character/{0}/{1}/soulbinds";

        public override async Task Run(params string[] data)
        {
            var query = JsonConvert.DeserializeObject<SchedulerCharacterQuery>(data[0]) ??
                        throw new InvalidJsonException(data[0]);
            using var shrug = CharacterLog(query);

            // Fetch API data
            ApiCharacterSoulbinds resultData;
            var uri = GenerateUri(query, ApiPath);
            try
            {
                var result = await GetJson<ApiCharacterSoulbinds>(uri);
                if (result.NotModified)
                {
                    LogNotModified();
                    return;
                }

                resultData = result.Data;
            }
            catch (HttpRequestException e)
            {
                Logger.Error("HTTP {0}", e.Message);
                return;
            }

            // Fetch character data
            var shadowlands = await Context.PlayerCharacterShadowlands.FindAsync(query.CharacterId);
            if (shadowlands == null)
            {
                shadowlands = new PlayerCharacterShadowlands
                {
                    CharacterId = query.CharacterId,
                };
                Context.PlayerCharacterShadowlands.Add(shadowlands);
            }

            shadowlands.CovenantId = resultData.ChosenCovenant?.Id ?? 0;
            shadowlands.RenownLevel = resultData.RenownLevel;

            var soulbind = resultData.Soulbinds?.FirstOrDefault(s => s.IsActive);
            if (soulbind != null)
            {
                shadowlands.SoulbindId = soulbind.Soulbind.Id;

                var conduits = soulbind.Traits
                    .EmptyIfNull()
                    .Where(t => t.Conduit?.Socket != null)
                    .OrderBy(t => t.Tier)
                    .ToArray();
                
                shadowlands.ConduitIds = conduits
                    .EmptyIfNull()
                    .Select(c => c.Conduit.Socket.Conduit.Id)
                    .ToList();
                
                shadowlands.ConduitRanks = conduits
                    .EmptyIfNull()
                    .Select(c => c.Conduit.Socket.Rank)
                    .ToList();
            }
            else
            {
                shadowlands.SoulbindId = 0;
                shadowlands.ConduitIds = new List<int>();
                shadowlands.ConduitRanks = new List<int>();
            }

            await Context.SaveChangesAsync();
        }
    }
}
