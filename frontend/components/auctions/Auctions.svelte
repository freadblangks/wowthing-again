<script lang="ts">
    import { afterUpdate } from 'svelte'

    import getSavedRoute from '@/utils/get-saved-route'
    import type { MultiSlugParams } from '@/types'

    import Sidebar from './AuctionsSidebar.svelte'
    import View from './AuctionsView.svelte'

    export let params: MultiSlugParams

    afterUpdate(() => getSavedRoute('auctions', params.slug1))
</script>

<Sidebar />
{#if params.slug1}
    <View {params} />
{/if}
