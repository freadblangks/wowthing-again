<script lang="ts">
    import {data as settingsData} from '@/stores/settings'

    import Checkbox from '@/components/forms/CheckboxInput.svelte'
</script>

<style lang="scss">
    .armor-type {
        h4 {
            display: inline-block;
            top: 50%;
            transform: translateY(-55%);
            width: 4.5rem;
        }

        :global(fieldset) {
            display: inline-block;
            width: 8.8rem;
        }
    }
    .separator {
        border-top: 1px dashed $border-color;
        margin-bottom: 0.25rem;
    }
</style>

<div class="thing-container settings-container">
    <h2>Transmog</h2>

    <div class="setting">
        <Checkbox
            name="transmog_completionistMode"
            bind:value={$settingsData.transmog.completionistMode}
        >Completionist Mode</Checkbox>
        <p>
            <strong class="status-shrug">WARNING!</strong>
            This will only treat a transmog item appearance as collected if you have collected
            that exact source, not any other item that shares the same appearance.
        </p>
    </div>

    <h3>Included Items</h3>

    <div class="armor-type">
        <h4>Cloth</h4>

        <Checkbox
            name="transmog_showMage"
            bind:value={$settingsData.transmog.showMage}
            textClass="class-mage"
        >Mage</Checkbox>

        <Checkbox
            name="transmog_showPriest"
            bind:value={$settingsData.transmog.showPriest}
            textClass="class-priest"
        >Priest</Checkbox>

        <Checkbox
            name="transmog_showWarlock"
            bind:value={$settingsData.transmog.showWarlock}
            textClass="class-warlock"
        >Warlock</Checkbox>
    </div>

    <div class="armor-type">
        <h4>Leather</h4>

        <Checkbox
            name="transmog_showDemonHunter"
            bind:value={$settingsData.transmog.showDemonHunter}
            textClass="class-demon-hunter"
        >Demon Hunter</Checkbox>
        <Checkbox
            name="transmog_showDruid"
            bind:value={$settingsData.transmog.showDruid}
            textClass="class-druid"
        >Druid</Checkbox>
        <Checkbox
            name="transmog_showMonk"
            bind:value={$settingsData.transmog.showMonk}
            textClass="class-monk"
        >Monk</Checkbox>
        <Checkbox
            name="transmog_showRogue"
            bind:value={$settingsData.transmog.showRogue}
            textClass="class-rogue"
        >Rogue</Checkbox>
    </div>

    <div class="armor-type">
        <h4>Mail</h4>

        <Checkbox
            name="transmog_showHunter"
            bind:value={$settingsData.transmog.showHunter}
            textClass="class-hunter"
        >Hunter</Checkbox>
        <Checkbox
            name="transmog_showShaman"
            bind:value={$settingsData.transmog.showShaman}
            textClass="class-shaman"
        >Shaman</Checkbox>
    </div>

    <div class="armor-type">
        <h4>Plate</h4>

        <Checkbox
            name="transmog_showDeathKnight"
            bind:value={$settingsData.transmog.showDeathKnight}
            textClass="class-death-knight"
        >Death Knight</Checkbox>
        <Checkbox
            name="transmog_showPaladin"
            bind:value={$settingsData.transmog.showPaladin}
            textClass="class-paladin"
        >Paladin</Checkbox>
        <Checkbox
            name="transmog_showWarrior"
            bind:value={$settingsData.transmog.showWarrior}
            textClass="class-warrior"
        >Warrior</Checkbox>
    </div>

    <div class="separator"></div>

    <div class="armor-type">
        <h4>Faction</h4>

        <Checkbox
            name="transmog_showAllianceOnly"
            bind:value={$settingsData.transmog.showAllianceOnly}
            textClass="faction-alliance"
        >Alliance only</Checkbox>

        <Checkbox
            name="transmog_showHordeOnly"
            bind:value={$settingsData.transmog.showHordeOnly}
            textClass="faction-horde"
        >Horde only</Checkbox>
    </div>
</div>
