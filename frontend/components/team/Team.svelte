<script lang="ts">
    import { location } from 'svelte-spa-router'

    import { data as teamData } from '@/stores/team'

    import CharacterName from './CharacterName.svelte'
    import CharacterNote from './CharacterNote.svelte'
    import CharacterCovenant from '@/components/common/CharacterCovenant.svelte'
    import GearItems from '@/components/gear/GearTableRowItems.svelte'
    import ClassIcon from '@/components/images/ClassIcon.svelte'
    import RaceIcon from '@/components/images/RaceIcon.svelte'
</script>

<style lang="scss">
    div {
        padding: 0.5rem;
    }
    .item-level {
        padding-left: 0.5rem;
    }
</style>

<div class="thing-container">
    <h2>[flag] {$teamData.name}</h2>
    <p>{$teamData.description}</p>
    <table class="table-striped2">
        <tbody>
            {#each $teamData.characters as teamCharacter}
                <tr class="faction{teamCharacter.character.faction}">
                    <td>
                        <RaceIcon character={teamCharacter.character} />
                        <ClassIcon character={teamCharacter.character} />
                    </td>
                    <CharacterName {teamCharacter} />
                    <td
                        class="item-level quality{teamCharacter.character
                            .calculatedItemLevelQuality}"
                        >{teamCharacter.character.calculatedItemLevel}</td
                    >
                    {#if $location === '/' || $location === '/gear'}
                        <GearItems
                            character={teamCharacter.character}
                            rowspan={2}
                            highlightMissingEnchants={false}
                            highlightMissingGems={false}
                        />
                    {/if}
                </tr>
                <tr class="faction{teamCharacter.character.faction}">
                    <td>Roles</td>
                    <CharacterNote {teamCharacter} />
                    <td>
                        <CharacterCovenant
                            character={teamCharacter.character}
                        />
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>
