import asyncio

async def run_chain_on_text(text: str, input_id: str):
    # Step 1: analysis (simple summary)
    analysis = {'summary': text[:200]}
    await asyncio.sleep(0)  # placeholder for async I/O
    # Step 2: transform (keywords)
    tokens = text.split()
    transformed = {'keywords': tokens[:10]}
    # Step 3: validate (naive)
    validated = True
    return {'analysis': analysis, 'transformed': transformed, 'validated': validated}
