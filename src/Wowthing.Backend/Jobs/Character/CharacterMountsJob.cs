﻿using System.Net.Http;
using Wowthing.Backend.Models.API.Character;
using Wowthing.Lib.Models.Player;
using Wowthing.Lib.Models.Query;

namespace Wowthing.Backend.Jobs.Character
{
    public class CharacterMountsJob : JobBase
    {
        private const string ApiPath = "profile/wow/character/{0}/{1}/collections/mounts";

        public override async Task Run(params string[] data)
        {
            var query = JsonConvert.DeserializeObject<SchedulerCharacterQuery>(data[0]) ??
                        throw new InvalidJsonException(data[0]);
            using var shrug = CharacterLog(query);

            // Fetch API data
            ApiCharacterMounts resultData;
            var uri = GenerateUri(query, ApiPath);
            try {
                var result = await GetJson<ApiCharacterMounts>(uri);
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
            var mounts = await Context.PlayerCharacterMounts.FindAsync(query.CharacterId);
            if (mounts == null)
            {
                mounts = new PlayerCharacterMounts
                {
                    CharacterId = query.CharacterId,
                };
                Context.PlayerCharacterMounts.Add(mounts);
            }

            mounts.Mounts = resultData.Mounts
                .Select(m => m.Mount.Id)
                .ToList();
            
            await Context.SaveChangesAsync();
        }
    }
}
