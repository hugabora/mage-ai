import BasePage from '@components/BasePage';
import SignForm from '@components/Sessions/SignForm';

function SignInPage() {
  return (
    <BasePage title="Sign in (Local)">
      <SignForm
        title="👋 Sign in (Local)"
        forceLocal
      />
    </BasePage>
  );
}

SignInPage.getInitialProps = async () => ({});

export default SignInPage;
