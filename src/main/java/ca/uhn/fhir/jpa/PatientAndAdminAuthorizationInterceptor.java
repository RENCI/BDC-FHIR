package ca.uhn.fhir.jpa;

import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.codec.binary.Base64;
import org.hl7.fhir.r4.model.IdType;

import ca.uhn.fhir.i18n.Msg;
import ca.uhn.fhir.interceptor.api.Hook;
import ca.uhn.fhir.interceptor.api.Interceptor;
import ca.uhn.fhir.rest.api.server.RequestDetails;
import ca.uhn.fhir.rest.server.exceptions.AuthenticationException;
import ca.uhn.fhir.rest.server.interceptor.InterceptorAdapter;
import ca.uhn.fhir.rest.server.interceptor.auth.AuthorizationInterceptor;
import ca.uhn.fhir.rest.server.interceptor.auth.IAuthRule;
import ca.uhn.fhir.rest.server.interceptor.auth.RuleBuilder;

@SuppressWarnings("ConstantConditions")
public class PatientAndAdminAuthorizationInterceptor extends AuthorizationInterceptor {

    @Override
    public List<IAuthRule> buildRuleList(RequestDetails theRequestDetails) {

        // Process authorization header - The following is a fake
        // implementation. Obviously we'd want something more real
        // for a production scenario.
        //
        // In this basic example we have two hardcoded bearer tokens,
        // one which is for a user that has access to one patient, and
        // another that has full access.
        String authHeader = theRequestDetails.getHeader("Authorization");

        boolean userIsAdmin = false;
        boolean userIsPublic = false;
        String username = "";
        String password = "";
        if (authHeader != null) {
            String base64 = authHeader.substring("Basic ".length());
            String base64decoded = new String(Base64.decodeBase64(base64));
            String[] parts = base64decoded.split(":");

            username = parts[0];
            password = parts[1];

        }

        if (username.equals("") && password.equals("")) {
            // This user has access to everything
            userIsAdmin = true;
        } else {
            // Throw an HTTP 401
            // throw new AuthenticationException(Msg.code(644) + "Missing or invalid
            // Authorization header value");
            userIsPublic = true;
        }

        if (userIsPublic) {
            // return new RuleBuilder().allowAll().build();

            return new RuleBuilder().allow("Allow Reads").read().allResources().withAnyId().andThen()
                    .allow().metadata().andThen()
                    .denyAll("Deny Public Writes").build();
        }

        // If the user is an admin, allow everything
        if (userIsAdmin) {
            return new RuleBuilder().allowAll().build();
        }

        // By default, deny everything. This should never get hit, but it's
        // good to be defensive
        return new RuleBuilder().denyAll().build();
    }
}