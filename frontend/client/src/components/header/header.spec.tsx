import { expect, test } from 'vitest'
import { render } from 'vitest-browser-react'
import Header from './header.component'
import { MemoryRouter } from 'react-router';

const testTitle = "HELLO WORLD!";

test('renders name', async () => {
  const { getByText } = render(<MemoryRouter><Header title={testTitle}/></MemoryRouter>)

  await expect.element(getByText(testTitle)).toBeInTheDocument();

  // await expect.element(getByText('Hello Vitest x2!')).toBeInTheDocument();
})
