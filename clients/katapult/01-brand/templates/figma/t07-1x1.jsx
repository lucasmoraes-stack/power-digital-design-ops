const imgAdobeStock4022200351 = "assets/d7ef2fc1-7e95-4924-a355-0a77dc72f2ad.png";
const imgSoftCircleBg = "assets/60773239-0c12-44a1-a3ea-63faa83f321f.svg";
const imgKatapultLogoWhite = "assets/b0334aba-a6aa-4424-aca8-9753e356a2c8.svg";

export default function Template07TopBlockRoundedCard() {
  return (
    <div className="bg-[#ed5370] relative size-full" data-node-id="547:1135" data-name="template-07-top-block-rounded-card">
      <div className="absolute left-[144px] size-[913px] top-[600px]" data-node-id="547:1136" data-name="soft-circle-bg">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgSoftCircleBg} />
      </div>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[48px] items-center left-[calc(50%-0.5px)] top-[66px]" data-node-id="547:1137">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="547:1138">
          <div className="h-[31.616px] relative shrink-0 w-[142px]" data-node-id="547:1139" data-name="Katapult Logo (White)">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgKatapultLogoWhite} />
          </div>
        </div>
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[0] not-italic relative shrink-0 text-[120px] text-center text-white tracking-[-4.8px] w-[1237px]" data-node-id="547:1145">
          <p className="leading-[0.9] mb-0">Your upgrade</p>
          <p className="leading-[0.9]">starts here.</p>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] whitespace-nowrap" data-node-id="547:1146">
          No credit score needed. Just tap and say yes.
        </p>
        <div className="bg-[#131540] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1147" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1147;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-[calc(50%-405.5px)] not-italic text-[15px] text-white top-[1143px] w-[811px]" data-node-id="547:1148">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="-translate-x-1/2 absolute h-[487px] left-1/2 top-[636px] w-[726px]" data-node-id="547:1149" data-name="AdobeStock_402220035 1">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[161.26%] left-[-12.59%] max-w-none top-[-30.59%] w-[125.08%]" src={imgAdobeStock4022200351} />
        </div>
      </div>
    </div>
  );
}